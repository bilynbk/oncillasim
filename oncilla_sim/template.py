# Oncilla Simulation Wizard
import os
import sys
import string
import shutil

from git import *

class Template:
    verbose = True
    tmpl_path = ''
    ow_path = ''
    onc_path = ''
    cca_path = ''
    data_path = ''
    
    def __init__(self, path, verbosity=True):
        self.verbose = verbosity
        self.tmpl_path = path
        
        self.ow_path = os.path.join(path, 'liboncilla-webots')
        self.onc_path = os.path.join(path, 'liboncilla')
        self.cca_path = os.path.join(path, 'cca-oncilla')
        self.data_path = os.path.join(self.ow_path, 'webots-data')
        
    def prepare(self):
        if not self.isEmpty():
            if self.isATemplateFolder():
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
        
    def create(self):
        print 'Provide_project_template'
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
        fo = open(self.data_path + "/worlds/Oncilla.wbt", "r+")
        world_orig = fo.read()
        for controller in examples:
            world = self.change_webots_controller(world_orig, controller)
            fn = open(os.path.join(target + "/worlds", controller + ".wbt"), "w+")
            fn.write(world)
            if self.verbose:
                print '* Created RCI Example:', target + "/worlds" + '/' + controller + ".wbt"
                         
    def change_webots_controller(self, world_orig, controller):
        old = '"None"'
        return string.replace(world_orig, old, '"' + controller + '"')
