# Oncilla Simulation Wizard
import os
import sys
import shutil

from template import WebotsTemplate

class WebotsProject:
    VERBOSE = True
    PROJECT_PATH = None
    TMP_PATH = None

    def __init__(self, path, verbose=True, clean=False):
        self.VERBOSE = verbose
        self.CLEAN = clean
        self.PROJECT_PATH = path

    def create(self, template):
        if self.VERBOSE:
            print 'Creating project at', self.PROJECT_PATH

        template.updateSkeleton(self.PROJECT_PATH)
        template.compilePluginsAndExamples(self.PROJECT_PATH)

    def update(self, template):
        if self.isEmpty():
            exit('''Error: The given folder is empty, can`t update.''')
        elif not self.isProjectFolder():
            exit('''Error: The given folder is not empty, but doesn`t seem to be a simulation project.''')

        if self.VERBOSE:
            print 'Updating project at', self.PROJECT_PATH

        # First we create a temporary new project
        template.updateSkeleton(self.PROJECT_PATH)
        template.compilePluginsAndExamples(self.PROJECT_PATH)

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
