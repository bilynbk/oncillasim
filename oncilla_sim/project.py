# Oncilla Simulation Wizard
import os
import sys
import shutil

from template import WebotsTemplate

class WebotsProject:
    VERBOSE = True
    PROJECT_PATH = None
    TMP_PATH = None
    REPO_LIST_FILE = ".oncilla-sim-wizard.list"
    REPO_MAKE_FILE = ".oncilla-sim-wizard.make"
    
    def __init__(self, path, verbose=True, clean=False):
        self.VERBOSE = verbose
        self.CLEAN = clean
        self.PROJECT_PATH = path
        self.TMP_PATH = os.path.join(self.PROJECT_PATH, '.tmp') 
        
    def create(self, template):
        if self.VERBOSE:
            print 'Creating project at', self.PROJECT_PATH
            
        if not self.isEmpty():
            if self.isProjectFolder():
                exit('''The given folder, seems to be a simulation project already. Try updating.''')
            else:
                exit('''The given folder is not empty, but doesn`t seem to be a simulation project. Try another path.''')
        else:
            template.createSkeleton(self.PROJECT_PATH)
            
            # TODO Loop through projects configured in the wizard
            self.rciexamples = template.createRCIExample(self.PROJECT_PATH)
            self.ccaexamples = template.createCCAExamples(self.PROJECT_PATH)
            self.compilePlugins()
            self.compileExamples()
        
    def update(self, template):
        if self.isEmpty():
            exit('''Error: The given folder is empty, can`t update.''') 
        elif not self.isProjectFolder():
            exit('''Error: The given folder is not empty, but doesn`t seem to be a simulation project.''') 
        
        if self.VERBOSE:
            print 'Updating project at', self.PROJECT_PATH
        
        # First we create a temporary new project
        if os.path.exists(self.TMP_PATH):
            shutil.rmtree(self.TMP_PATH)
        template.createSkeleton(self.TMP_PATH)
        
        # TODO Loop through projects configured in the wizard
        self.rciexamples = template.createRCIExample(self.TMP_PATH)
        self.ccaexamples = template.createCCAExamples(self.TMP_PATH)
        if self.VERBOSE:
            print 'Syncing', self.TMP_PATH, 'and', self.PROJECT_PATH
        template.syncDir(self.TMP_PATH, self.TMP_PATH, self.PROJECT_PATH)
        self.compilePlugins()
        self.compileExamples()
        if os.path.exists(self.TMP_PATH):
            shutil.rmtree(self.TMP_PATH)
        
    def isEmpty(self):
        if os.path.exists(self.PROJECT_PATH):
            return False
        else:
            return True
    
    """
    Check if given project folder actually contains a project
    """
    def isProjectFolder(self):
        if os.path.exists(os.path.join(self.PROJECT_PATH, 'controllers')) \
            or os.path.exists(os.path.join(self.PROJECT_PATH, 'worlds')) \
            or os.path.exists(os.path.join(self.PROJECT_PATH, 'plugins')):
            return True
        return False

    """
    Compiles the physics plugin, necessary for libwebots 
    """
    def compilePlugins(self):
        os.system('make --directory ' + self.PLUGIN_PATH)
        if self.VERBOSE:
            print 'Compiled physics plugin at', self.PLUGIN_PATH

    """
    Compiling all examples 
    """
    def compileExamples(self):
        if self.VERBOSE:
            print 'Compiling Examples'
        
        # TODO Loop through projects configured in the wizard
        for example in (self.rciexamples + self.ccaexamples):
            if self.CLEAN:
                if self.VERBOSE:
                    print '* Cleaning example', example
                os.system('make CLEAN --directory ' + os.path.join(self.CONTROLLER_PATH, example))
            
            if self.VERBOSE:
                print '* Compiling example', example
            
            # TODO Use makefile configured for the project
            os.system('make --directory ' + os.path.join(self.CONTROLLER_PATH, example))
            
            # Check, if controller was built
            if not os.path.exists(os.path.join(self.CONTROLLER_PATH, example, example)):
                exit('Error: Compilation of ' + example + ' failed.')
        print 'Examples successfully compiled. Open example world files with webots.'
