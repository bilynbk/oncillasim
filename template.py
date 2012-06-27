# Oncilla Simulation Wizard
import os
import sys
import string
import shutil
import filecmp

from git import *

class WebotsTemplate:
    verbose = True
    tmpl_path = None
    ow_path = None
    onc_path = None
    cca_path = None
    data_path = None
    tmp_path = None
    sync_ignore = False
    sync_overwrite = False
    foo = 0
    
    def __init__(self, path, verbosity=True):
        self.verbose = verbosity
        self.tmpl_path = path
        
        self.ow_path = os.path.join(path, 'liboncilla-webots')
        self.onc_path = os.path.join(path, 'liboncilla')
        self.cca_path = os.path.join(path, 'cca-oncilla')
        self.data_path = os.path.join(self.ow_path, 'webots-data')
        
    def prepare(self):
        if not self.isEmpty():
            if self.verbose:
                print 'Folder is not empty, checking if template already existing at', self.tmpl_path
            if self.isTemplateFolder():
                if self.verbose:
                    print 'Template is already existing. Looking for updates.'
                self.update()
            else:
                exit('''The template folder seems to contain other content. Try choosing a different template folder.''')
        else:
            if self.verbose:
                print 'Template folder is not existing yet. Creating.'
            self.create()
        
    def isEmpty(self):
        if os.path.exists(self.tmpl_path):
            return False
        else:
            return True
        
    def update(self):
        if self.verbose:
            print 'Updating project template at', self.tmpl_path        
        
        # Fetch updates for liboncilla-webots
        if self.verbose:
            print '* Updating skeleton from liboncilla-webots ...'
        # wrepo = Repo.init(path=self.ow_path) >3.2
        # wrepo.git.remote("update", "origin") >3.2
        g = Git(self.ow_path)
        g.execute(['git', 'pull', 'origin'])

        
        # Fetch updates for liboncilla for example 1
        if self.verbose:
            print '* Updating examples from liboncilla ...'
        #orepo = Repo.init(path=self.onc_path)
        #orepo.git.remote("update", "origin")
        g = Git(self.onc_path)
        g.execute(['git', 'pull', 'origin'])

        # Fetch updates for cca-oncilla for examples 2-4
        if self.verbose:
            print '* Updating examples from cca-oncilla ...'
        #crepo = Repo.init(path=self.cca_path)
        #crepo.git.remote("update", "origin")
        g = Git(self.cca_path)
        g.execute(['git', 'pull', 'origin'])
        
    def create(self):
        print 'Creating project template'
        os.makedirs(self.tmpl_path)
        
        # Make a blank checkout of liboncilla-webots
        print '* Cloning project template from liboncilla-webots ...'
        #wrepo = Repo.init() >3.2
        if not os.path.exists(self.ow_path):
            os.makedirs(self.ow_path)
        g = Git(self.ow_path)
        remote = "https://anordman@redmine.amarsi-project.eu/git/liboncilla-webots.git"
        g.execute(['git', 'clone', remote, self.ow_path])
        #wrepo.clone_from("https://anordman@redmine.amarsi-project.eu/git/liboncilla-webots.git",
        #                self.ow_path) >3.2
        
        # Make a blank checkout of liboncilla for example 1
        print '* Cloning examples from liboncilla ...'
        #orepo = Repo.init() >3.2
        #orepo.clone_from("https://anordman@redmine.amarsi-project.eu/git/quaddrivers.git",
        #                self.onc_path, None, b="dev") >3.2
        if not os.path.exists(self.onc_path):
            os.makedirs(self.onc_path)
        g = Git(self.onc_path)
        remote = "https://anordman@redmine.amarsi-project.eu/git/quaddrivers.git"
        g.execute(['git', 'clone', remote, self.onc_path])

        
        # Make a blank checkout of cca-oncilla for examples 2-4
        print '* Cloning examples from cca-oncilla ...'
        #crepo = Repo.init() >3.2
        #crepo.clone_from("https://anordman@redmine.amarsi-project.eu/git/oncilla-cca.git",
        #                self.cca_path) >3.2
        if not os.path.exists(self.cca_path):
            os.makedirs(self.cca_path)
        g = Git(self.cca_path)
        remote = "https://anordman@redmine.amarsi-project.eu/git/oncilla-cca.git"
        g.execute(['git', 'clone', remote, self.cca_path])
        
    def isTemplateFolder(self):
        for path in [self.ow_path, self.onc_path, self.cca_path, self.data_path]:
            if not os.path.exists(path):
                return False
        return True        
    
    def createSkeleton(self, target):
        if self.verbose:
            print '* Creating Project Skeleton'
        shutil.copytree(self.data_path,
            target,
            symlinks=False,
            ignore=shutil.ignore_patterns('.git*'))
            
    def updateSkeleton(self, target):
        if self.verbose:
            print '* Updating Project Skeleton'        
        self.syncDir(self.data_path, self.data_path, target)

    def createRCIExample(self, target):
        examples = ['Example1']
        for folder in examples:
            if not os.path.exists(target + '/controllers/' + folder):
                os.makedirs(target + '/controllers/' + folder)

        # Example source
        shutil.copy(self.onc_path + "/examples/SimpleSineMovement.cpp",
                target + '/controllers/' + examples[0] + '/' + examples[0] + '.cpp')
        
        # Makefile
        shutil.copy(self.data_path + '/controllers/with-rci/Makefile',
                        target + '/controllers/' + examples[0] + '/')
        
        # World files - we have to replace the controller in the world files
        for controller in examples:
            fn = open(os.path.join(target + "/worlds", controller + ".wbt"), "w+")
            fn.write(self.get_world_file_for(controller))
            if self.verbose:
                print '* Created RCI Example:', target + "/worlds" + '/' + controller + ".wbt"
                
        return examples

    def updateRCIExample(self, target):
        examples = ['Example1']
        for folder in examples:
            if not os.path.exists(target + '/controllers/' + folder):
                os.makedirs(target + '/controllers/' + folder)

        # Example source
        shutil.copy(self.onc_path + "/examples/SimpleSineMovement.cpp",
                self.tmp_path + '/controllers/' + examples[0] + '/' + examples[0] + '.cpp')
        
        # Makefile
        shutil.copy(self.data_path + '/controllers/with-rci/Makefile',
                self.tmp_path + '/controllers/' + examples[0] + '/')
        
        # World files - we have to replace the controller in the world files
        for controller in examples:
            fn = open(os.path.join(target + "/worlds", controller + ".wbt"), "w+")
            fn.write(self.get_world_file_for(controller))
            if self.verbose:
                print '* Created RCI Example:', target + "/worlds" + '/' + controller + ".wbt"
                
        return examples

    def createCCAExamples(self, target):
        examples = ['Example2']
        for folder in examples:
            if not os.path.exists(target + '/controllers/' + folder):
                os.makedirs(target + '/controllers/' + folder)

        # Example source
        shutil.copy(self.cca_path + "/cca-oncilla/examples/SimpleSineMovement-CCALocal.cpp",
                target + '/controllers/' + examples[0] + '/' + examples[0] + '.cpp')
        
        # Makefile
        shutil.copy(self.data_path + '/controllers/with-cca/Makefile',
                        target + '/controllers/' + examples[0] + '/')
        
        # World files - we have to replace the controller in the world files
        for controller in examples:
            fn = open(os.path.join(target + "/worlds", controller + ".wbt"), "w+")
            fn.write(self.get_world_file_for(controller))
            if self.verbose:
                print '* Created CCA Example:', target + "/worlds" + '/' + controller + ".wbt"
                
        return examples
                         
    def get_world_file_for(self, controller):
        fo = open(self.data_path + "/worlds/Oncilla.wbt.in", "r+")
        world_orig = fo.read()
        old = '@CONTROLLER@'
        return string.replace(world_orig, old, controller)
    
    def syncDir(self, syncdir, src, dest):
        self.foo = self.foo + 1 
        
        # If folder doesn't exist, create it 
        for root, dirs, files in os.walk(syncdir, topdown=False):
            for name in dirs:
                required_folder = os.path.join(dest, os.path.relpath(os.path.join(root, name), syncdir))
                if not os.path.exists(required_folder):
                    os.makedirs(required_folder)
                    if self.verbose:
                        print '** Created', required_folder

        # If file doesn exist, copy it
        # If file is the same, ignore it
        # If file is different, ask for solution
        for root, dirs, files in os.walk(syncdir, topdown=False):
            for name in files:
                # Ignore hidden and .in files
                if name.startswith(".") or name.endswith(".in"):
                    continue
                
                required_file = os.path.join(dest, os.path.relpath(os.path.join(root, name), syncdir))
                
                # File is new, copy it
                srcfile = os.path.join(root, name)
                destfile = required_file
                
                self.syncFile(srcfile, destfile)
                
    def syncFile(self, srcfile, destfile):
        if not os.path.exists(destfile):
            shutil.copyfile(srcfile, destfile)
            if self.verbose:
                print '** Copied', srcfile, ' to ', destfile
        else:
            # File exists, compare
            if filecmp.cmp(srcfile, destfile):
                # Files are the same, ignore
                return
            else:
                # Files not the same, handle that
                if self.sync_ignore:
                    return
                elif self.sync_overwrite:
                    shutil.copyfile(srcfile, destfile) # Overwrite file
                    if self.verbose:
                        print '** Copied', srcfile, ' to ', destfile
                else:
                    if self.askForOverwriting(destfile):
                        shutil.copyfile(srcfile, destfile) # Overwrite file
                        if self.verbose:
                            print '** Copied', srcfile, ' to ', destfile
                    else:
                        return
                            
    def askForOverwriting(self, filename):
        question = "File '" + filename + "' was edited locally, should we overwrite it?\n" + \
                   "[y] yes - [o] overwrite all - [n] ignore - [i] ignore all\n"
        prompt = '[y/o/N/i]'
                    
        valid = {"y":True, "o":True, "n":False, "i":False}
    
        while True:
            sys.stdout.write(str(question) + prompt)
            choice = raw_input().lower()
            
            if choice == 'i':
                self.sync_ignore = True
            elif choice == 'o':
                self.sync_overwrite = True
            
            if choice == '' or choice == 'n' or choice == 'i':
                return False
            elif choice == 'y' or choice == 'o':
                return True
            else:
                sys.stdout.write("Please respond with one of [y/o/N/i]")
