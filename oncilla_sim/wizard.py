# Oncilla Simulation Wizard
#
import os
import sys
from argparse import ArgumentParser

from project import WebotsProject
from template import WebotsTemplate

class Wizard:
    verbose = True
    online = True
    proj_path = ''
    tmpl_path = ''
    wbts_path = ''
    project = None
    template = None
    
    def __init__(self, path, verbose=True, online=True,
                tmpl_path='/tmp/oncillawizard/template',
                clean=False):
        self.verbose = verbose
        self.online = online
        self.proj_path = path
        self.tmpl_path = tmpl_path
        self.clean = clean
        
        self.getWebotsHome()
        
        self.project = WebotsProject(self.proj_path, verbose=verbose, clean=clean)
        self.template = WebotsTemplate(self.tmpl_path, verbose=verbose, online=online)
        
    def createProject(self):
        if not self.project.isEmpty():
            if self.project.isProjectFolder():
                exit('Error: Destination path seems to already contain a project, try updating.')
            else:
                exit('Error: Destination path is not empty, try another folder.')
        else:
            self.template.prepare()
            self.project.create(self.template)
        
    def updateProject(self):
        if self.verbose:
            print 'Updating project at', self.proj_path
        #exit('Error: Updating a project is not yet implemented.')
        self.template.prepare()
        self.project.update(self.template)
        
    def getWebotsHome(self):
        if self.verbose:
            print 'Trying to find webots ...'
        if (not 'WEBOTS_HOME' in os.environ) \
            or (len(os.environ['WEBOTS_HOME']) == 0):
            # Try common places
            self.wbts_path = '/usr/local/webots'
            if not os.path.exists(self.wbts_path):
                exit('Could not find WEBOTS_HOME')
            else:
                os.environ['WEBOTS_HOME'] = self.wbts_path
        else:
            self.wbts_path = os.environ['WEBOTS_HOME']
        if self.verbose:
            print 'Found webots at', self.wbts_path
         
def main():
    usage = "Usage: %prog [options] (create / update) path"
    parser = ArgumentParser()
    parser.add_argument("-q", "--quiet",
                  action="store_false", dest="verbose", default=True,
                  help="don't print status messages to stdout")
    parser.add_argument("-o", "--offline-mode",
                  action="store_false", dest="online", default=True,
                  help="just copy and compile, don`t update from online repositories")
    parser.add_argument("-c", "--clean",
                  action="store_true", dest="clean", default=False,
                  help="force a clean (re)compilation of all examples")
    parser.add_argument("-t", "--template_path",
                  dest="tmpl_path", default='/tmp/onc/tmpl',
                  help="specify folder to use for temporary files during project setup")
    parser.add_argument("command", help="command, either 'create' or 'update'")
    parser.add_argument("path", help="destination / path of the project")
    args = parser.parse_args()
    
    wizard = Wizard(args.path, verbose=args.verbose, online=args.online,
                tmpl_path=args.tmpl_path, clean=args.clean)
    
    if args.command == "create":
        wizard.createProject()
    elif args.command == "update":
        wizard.updateProject()
    else:
        parser.error("Unknown argument. Use either 'create' or 'update'.")

