# Oncilla Simulation Wizard
import os
import sys
import shutil

from template import Template

class Project:
    verbose = True
    proj_path = ''
    
    def __init__(self, path, verbosity=True):
        self.verbose = verbosity
        self.proj_path = path
        
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
            template.createRCIExample(self.proj_path)
        
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
