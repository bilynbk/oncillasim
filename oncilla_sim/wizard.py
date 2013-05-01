# Oncilla Simulation Wizard
#
import os
import sys
from argparse import ArgumentParser

from project import WebotsProject
from template import WebotsTemplate

class Wizard:
    VERBOSE = True
    ONLINE = True
    PROJECT_PATH = ''
    TEMPLATE_PATH = ''
    WEBOTS_PATH = ''
    PROJECT = None
    TEMPLATE = None
    
    def __init__(self, path, verbose=True, online=True,
                tmpl_path='/tmp/oncillawizard/template',
                clean=False):
        self.VERBOSE = verbose
        self.ONLINE = online
        self.PROJECT_PATH = path
        self.TEMPLATE_PATH = tmpl_path
        self.CLEAN = clean
        
        self.getWebotsHome()
        
        self.PROJECT = WebotsProject(self.PROJECT_PATH, verbose=verbose, clean=clean)
        self.TEMPLATE = WebotsTemplate(self.TEMPLATE_PATH, verbose=verbose, online=online)
        
    def createProject(self):
        if not self.PROJECT.isEmpty():
            if self.PROJECT.isProjectFolder():
                exit('Error: Destination path seems to already contain a project, try updating.')
            else:
                exit('Error: Destination path is not empty, try another folder.')
        else:
            self.TEMPLATE.prepare()
            self.PROJECT.create(self.TEMPLATE)
        
    def updateProject(self):
        if self.VERBOSE:
            print 'Updating PROJECT at', self.PROJECT_PATH
        #exit('Error: Updating a PROJECT is not yet implemented.')
        self.TEMPLATE.prepare()
        self.PROJECT.update(self.TEMPLATE)
        
    def getWebotsHome(self):
        if self.VERBOSE:
            print 'Trying to find webots ...'
        if (not 'WEBOTS_HOME' in os.environ) \
            or (len(os.environ['WEBOTS_HOME']) == 0):
            print '... WEBOTS_HOME environment variable is not set.'
            
            # Try common places
            self.WEBOTS_PATH = '/usr/local/webots'
            if not os.path.exists(self.WEBOTS_PATH):
                exit('Could not find WEBOTS_HOME')
            else:
                os.environ['WEBOTS_HOME'] = self.WEBOTS_PATH
        else:
            self.WEBOTS_PATH = os.environ['WEBOTS_HOME']
        if self.VERBOSE:
            print '... found webots at', self.WEBOTS_PATH
         
def main():
    DEFAULT_TEMPLATE_PATH = '/tmp/onc/tmpl'
    
    usage = "Usage: %prog [options] (create / update) path"
    parser = ArgumentParser()
    parser.add_argument("-q", "--quiet",
                  action="store_false", dest="VERBOSE", default=True,
                  help="don't print status messages to stdout")
    parser.add_argument("-o", "--offline-mode",
                  action="store_false", dest="ONLINE", default=True,
                  help="just copy and compile, don`t update from online repositories")
    parser.add_argument("-c", "--clean",
                  action="store_true", dest="CLEAN", default=False,
                  help="force a clean (re)compilation of all examples")
    parser.add_argument("-t", "--template_path",
                  dest="TEMPLATE_PATH", default=DEFAULT_TEMPLATE_PATH,
                  help="specify folder to use for temporary files during project setup")
    parser.add_argument("command", help="command, either 'create' or 'update'")
    parser.add_argument("path", help="destination / path of the project")
    args = parser.parse_args()
    
    wizard = Wizard(args.path, verbose=args.VERBOSE, online=args.ONLINE,
                tmpl_path=args.TEMPLATE_PATH, clean=args.CLEAN)
    
    if args.command == "create":
        wizard.createProject()
    elif args.command == "update":
        wizard.updateProject()
    else:
        parser.error("Unknown argument. Use either 'create' or 'update'.")

