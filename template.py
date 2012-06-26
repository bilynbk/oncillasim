# Oncilla Simulation Wizard
import os
import sys
import string
import shutil

from git import *

class WebotsTemplate:
    verbose = True
    tmpl_path = None
    ow_path = None
    onc_path = None
    cca_path = None
    data_path = None
    
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
            print 'Updating project template'        
        
        # Fetch updates for liboncilla-webots
        if self.verbose:
            print '* Updating skeleton from liboncilla-webots ...'
        wrepo = Repo.init(path=self.ow_path)
        wrepo.git.remote("update", "origin")
        
        # Fetch updates for liboncilla for example 1
        if self.verbose:
            print '* Updating examples from liboncilla ...'
        orepo = Repo.init()
        wrepo.git.remote("update", "origin")

        # Fetch updates for cca-oncilla for examples 2-4
        if self.verbose:
            print '* Updating examples from cca-oncilla ...'
        crepo = Repo.init()
        crepo.git.remote("update", "origin")
        
    def create(self):
        print 'Creating project template'
        os.makedirs(self.tmpl_path)
        
        # Make a blank checkout of liboncilla-webots
        print '* Cloning project template from liboncilla-webots ...'
        wrepo = Repo.init()
        wrepo.clone_from("https://anordman@redmine.amarsi-project.eu/git/liboncilla-webots.git",
                        self.ow_path)
        
        # Make a blank checkout of liboncilla for example 1
        print '* Cloning examples from liboncilla ...'
        orepo = Repo.init()
        orepo.clone_from("https://anordman@redmine.amarsi-project.eu/git/quaddrivers.git",
                        self.onc_path, None, b="dev")
        
        # Make a blank checkout of cca-oncilla for examples 2-4
        print '* Cloning examples from cca-oncilla ...'
        crepo = Repo.init()
        crepo.clone_from("https://anordman@redmine.amarsi-project.eu/git/oncilla-cca.git",
                        self.cca_path)
        
    def isTemplateFolder(self):
        for path in [self.ow_path, self.onc_path, self.cca_path, self.data_path]:
            if not os.path.exists(path):
                return False
        return True        
    
    def createSkeleton(self, target):
        shutil.copytree(self.data_path,
            target,
            symlinks=False,
            ignore=shutil.ignore_patterns('.git*'))
        if self.verbose:
            print '* Created Project Skeleton'
    
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
