#!/usr/bin/env python
#
# Oncilla Simulation Wizard
#
import os
import sys
from argparse import ArgumentParser

from project import Project
from template import Template

class Wizard:
    verbose = True
    proj_path = ''
    tmpl_path = ''
    wbts_path = ''
    project = None
    template = None
    
    def __init__(self, path, verbosity=True):
        self.verbose = verbosity
        self.proj_path = path
        self.tmpl_path = '/tmp/oncillawizard/template'
        
        self.getWebotsHome()
        
        self.project = Project(self.proj_path)
        self.template = Template(self.tmpl_path)
        
    def createProject(self):
        if not self.project.isEmpty():
            exit('Project path is not empty. Try updating.')
        else:
            self.template.prepare()
            self.project.create(self.template)
        
    def updateProject(self):
        if self.verbose:
            print 'Updating project at', self.proj_path
        if self.project.isEmpty():
            exit('Project path doesn`t point to a valid simulation project. Can`t update.')
        else:
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
        print 'Found webots at',self.wbts_path
         
def main():
    usage = "Usage: %prog [options] (create_project / update_project) path"
    parser = ArgumentParser()
    parser.add_argument("-q", "--quiet", action='count', help="be quiet")
    parser.add_argument("command", help="command, either 'create' or 'update'")
    parser.add_argument("path", help="path / destination of the project")
    args = parser.parse_args()
    
    wizard = Wizard(args.path)
    
    if args.command == "create":
        wizard.createProject()
    elif args.command == "update":
        wizard.updateProject()
    else:
        parser.error("Unknown argument. Use either 'create_project' or 'update_project'.")

if __name__ == '__main__':
    main()
