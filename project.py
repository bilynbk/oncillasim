# Oncilla Simulation Wizard
import os
import sys
import shutil

from template import WebotsTemplate

class WebotsProject:
    verbose = True
    proj_path = ''
    ctrl_path = ''
    plugin_path = ''
    worlds_path = ''
    rciexamples = None
    ccaexamples = None
    
    def __init__(self, path, verbosity=True):
        self.verbose = verbosity
        self.proj_path = path
        self.ctrl_path = os.path.join(path, 'controllers')
        self.worlds_path = os.path.join(path, 'worlds')
        self.plugin_path = os.path.join(path, 'plugins/physics/liboncilla-webots-plugin')
        
    def create(self, template):
        if self.verbose:
            print 'Creating project at', self.proj_path
            
        if not self.isEmpty():
            if self.isASimulationProject():
                exit('''The given folder, seems to be a simulation project already. Try updating.''')
            else:
                exit('''The given folder is not empty, but doesn`t seem to be a simulation project. Try another path.''')
        else:
            template.createSkeleton(self.proj_path)
            self.rciexamples = template.createRCIExample(self.proj_path)
            self.ccaexamples = template.createCCAExamples(self.proj_path)
            self.compilePlugins()
            self.compileExamples()
        
    def update(self, template):
        if self.verbose:
            print 'Updating project at', self.proj_path
        
    def isEmpty(self):
        if os.path.exists(self.proj_path):
            return False
        else:
            return True
    
    """
    Check, if the given path is a valid simulation project. Features are for
    example, required folders
    """
    def isASimulationProject(self):
        if self.isEmpty():
            return False
        if not os.path.exists(os.path.join(self.proj_path, 'worlds')):
            return False
        if not os.path.exists(os.path.join(self.proj_path, 'plugins')):
            return False
        if not os.path.exists(os.path.join(self.proj_path, 'controllers')):
            return False

    """
    Compiles the physics plugin, necessary for libwebots 
    """
    def compilePlugins(self):
        os.system('make --directory ' + self.plugin_path)
        if self.verbose:
            print 'Compiled physics plugin at', self.plugin_path

    """
    Compiling all examples 
    """
    def compileExamples(self):  
        if self.verbose:
            print 'Compiling Examples'
        for example in self.rciexamples:
            print '* Compiling RCI example', example
            os.system('make --directory '+os.path.join(self.ctrl_path, example))
        for example in self.ccaexamples:
            print '* Compiling CCA example', example
            os.system('make --directory '+os.path.join(self.ctrl_path, example))
            
