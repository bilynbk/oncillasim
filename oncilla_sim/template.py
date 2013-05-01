# Oncilla Simulation Wizard
import os
import sys
import string
import shutil
import filecmp
import ConfigParser

from git import *

class WebotsTemplate:
    VERBOSE = True
    ONLINE = True
    TEMPLATE_PATH = None
    TMP_PATH = None
    SYNC_IGNORE = False
    SYNC_OVERWRITE = False

    def __init__(self, path, verbose=True, online=True):
        self.VERBOSE = verbose
        self.ONLINE = online
        self.TEMPLATE_PATH = path
        
        self.ow_path = os.path.join(path, 'liboncilla-webots')
        self.onc_path = os.path.join(path, 'liboncilla')
        self.cca_path = os.path.join(path, 'cca-oncilla')
        self.data_path = os.path.join(self.ow_path, 'webots-data')

        config = ConfigParser.RawConfigParser()
        config.read(['wizard.cfg',
                     '/usr/local/share/oncilla-sim/wizard.cfg',
                     '/usr/share/oncilla-sim/wizard.cfg'])
        
        print "+++++++++++"
        print config.sections()
        
        self.onc_remote = config.get('liboncilla', 'remote')
        self.onc_tag = config.get('liboncilla', 'tag')
        self.ow_remote = config.get('liboncilla-webots', 'remote')
        self.ow_tag = config.get('liboncilla-webots', 'tag')
        self.cca_remote = config.get('libcca-oncilla', 'remote')
        self.cca_tag = config.get('libcca-oncilla', 'tag')

    def prepare(self):
        if not self.isEmpty():
            if self.VERBOSE:
                print 'Folder is not empty, checking if template already existing at', self.TEMPLATE_PATH
            if self.isTemplateFolder():
                if self.VERBOSE:
                    print 'Template is already existing. Looking for updates.'
                if self.ONLINE:
                    self.update()
            else:
                exit('''The template folder seems to contain other content. Try choosing a different template folder.''')
        else:
            if self.VERBOSE:
                print 'Template folder is not existing yet. Creating.'
            if not self.ONLINE:
                exit('Error: I need to fetch the project template, but I am in offline mode.')
            self.create()
        
    def isEmpty(self):
        if os.path.exists(self.TEMPLATE_PATH):
            return False
        else:
            return True
        
    def update(self):
        if self.VERBOSE:
            print 'Updating project template at', self.TEMPLATE_PATH        
        
        # Fetch updates for liboncilla-webots
        if self.VERBOSE:
            print '* Updating skeleton from liboncilla-webots ...'
        g = Git(self.ow_path)
        g.execute(['git', 'fetch', '--all'])
        g.execute(['git', 'fetch', '--tags'])
        g.checkout(self.ow_tag)
        
        # Fetch updates for liboncilla for example 1
        if self.VERBOSE:
            print '* Updating examples from liboncilla ...'
        g = Git(self.onc_path)
        g.execute(['git', 'fetch', '--all'])
        g.execute(['git', 'fetch', '--tags'])
        g.checkout(self.onc_tag)
        
        # Fetch updates for cca-oncilla for examples 2-4
        if self.VERBOSE:
            print '* Updating examples from cca-oncilla ...'
        g = Git(self.cca_path)
        g.execute(['git', 'fetch', '--all'])
        g.execute(['git', 'fetch', '--tags'])
        g.checkout(self.cca_tag)

    def create(self):
        if self.VERBOSE:
            print 'Creating project template'
        os.makedirs(self.TEMPLATE_PATH)
        
        # Make a blank checkout of liboncilla-webots
        if self.VERBOSE:
            print '* Cloning project template from liboncilla-webots ...'

        if not os.path.exists(self.ow_path):
            os.makedirs(self.ow_path)
        g = Git(self.ow_path)
        g.execute(['git', 'clone', self.ow_remote, self.ow_path])
        g.execute(['git', 'fetch', '--all'])
        g.execute(['git', 'fetch', '--tags'])
        g.checkout(self.ow_tag)
        
        # Make a blank checkout of liboncilla for example 1
        if self.VERBOSE:
            print '* Cloning examples from liboncilla ...'
        if not os.path.exists(self.onc_path):
            os.makedirs(self.onc_path)
        g = Git(self.onc_path)
        g.execute(['git', 'clone', self.onc_remote, self.onc_path])
        g.execute(['git', 'fetch', '--all'])
        g.execute(['git', 'fetch', '--tags'])
        g.checkout(self.onc_tag)
        
        # Make a blank checkout of cca-oncilla for examples 2-4
        if self.VERBOSE:
            print '* Cloning examples from cca-oncilla ...'
        if not os.path.exists(self.cca_path):
            os.makedirs(self.cca_path)
        g = Git(self.cca_path)
        g.execute(['git', 'clone', self.cca_remote, self.cca_path])
        g.execute(['git', 'fetch', '--all'])
        g.execute(['git', 'fetch', '--tags'])
        g.checkout(self.cca_tag)
        
    def isTemplateFolder(self):
        for path in [self.ow_path, self.onc_path, self.cca_path, self.data_path]:
            if not os.path.exists(path):
                return False
        return True        
    
    def createSkeleton(self, target):
        if self.VERBOSE:
            print '* Creating Project Skeleton'
        shutil.copytree(self.data_path,
            target,
            symlinks=False,
            ignore=shutil.ignore_patterns('.git*'))
            
    def updateSkeleton(self, target):
        if self.VERBOSE:
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
            if self.VERBOSE:
                print '* Created RCI Example:', target + "/worlds" + '/' + controller + ".wbt"
                
        return examples


    def createCCAExamples(self, target):
        examples = ['Example2', 'Example3']
        for folder in examples:
            if not os.path.exists(target + '/controllers/' + folder):
                os.makedirs(target + '/controllers/' + folder)

        # Local Example source
        shutil.copy(self.cca_path + "/cca-oncilla/examples/Local-SimpleSineMovement.cpp",
                target + '/controllers/' + examples[0] + '/' + examples[0] + '.cpp')
        # Makefile
        shutil.copy(self.data_path + '/controllers/with-cca/Makefile',
                        target + '/controllers/' + examples[0] + '/')
        
        # Remote Example sources
        shutil.copy(self.cca_path + "/cca-oncilla/examples/Remote-Oncilla.cpp",
                target + '/controllers/' + examples[1] + '/' + examples[1] + '.cpp')
        # Makefile
        shutil.copy(self.data_path + '/controllers/with-cca/Makefile',
                        target + '/controllers/' + examples[1] + '/')
        
        # World files - we have to replace the controller in the world files
        for controller in examples:
            fn = open(os.path.join(target + "/worlds", controller + ".wbt"), "w+")
            fn.write(self.get_world_file_for(controller))
            if self.VERBOSE:
                print '* Created CCA Example:', target + "/worlds" + '/' + controller + ".wbt"
                
        return examples
                         
    def get_world_file_for(self, controller):
        fo = open(self.data_path + "/worlds/Oncilla.wbt.in", "r+")
        world_orig = fo.read()
        old = '@CONTROLLER@'
        return string.replace(world_orig, old, controller)
    
    def syncDir(self, syncdir, src, dest):
        
        # If folder doesn't exist, create it 
        for root, dirs, files in os.walk(syncdir, topdown=False):
            for name in dirs:
                required_folder = os.path.join(dest, os.path.relpath(os.path.join(root, name), syncdir))
                if not os.path.exists(required_folder):
                    os.makedirs(required_folder)
                    if self.VERBOSE:
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
            if self.VERBOSE:
                print '** Copied', srcfile, ' to ', destfile
        else:
            # File exists, compare
            if filecmp.cmp(srcfile, destfile):
                # Files are the same, ignore
                return
            else:
                # Files not the same, handle that
                if self.SYNC_IGNORE:
                    return
                elif self.SYNC_OVERWRITE:
                    shutil.copyfile(destfile, destfile+'.backup') # Backup
                    shutil.copyfile(srcfile, destfile) # Overwrite file
                    if self.VERBOSE:
                        print '** Copied', srcfile, ' to ', destfile
                else:
                    if self.askForOverwriting(destfile):
                        shutil.copyfile(srcfile, destfile) # Overwrite file
                        if self.VERBOSE:
                            print '** Copied', srcfile, ' to ', destfile
                    else:
                        return
                            
    def askForOverwriting(self, filename):
        question = "Local file '" + filename + "' differs from template file,"+\
                   " should we overwrite it?\n" + \
                   "[y] yes - [o] overwrite all - [n] ignore - [i] ignore all\n"
        prompt = '[y/o/N/i]'
                    
        valid = {"y":True, "o":True, "n":False, "i":False}
    
        while True:
            sys.stdout.write(str(question) + prompt)
            choice = raw_input().lower()
            
            if choice == 'i':
                self.SYNC_IGNORE = True
            elif choice == 'o':
                self.SYNC_OVERWRITE = True
            
            if choice == '' or choice == 'n' or choice == 'i':
                return False
            elif choice == 'y' or choice == 'o':
                return True
            else:
                sys.stdout.write("Please respond with one of [y/o/N/i]")
