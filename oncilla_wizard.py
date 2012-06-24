#!/usr/bin/env python
#
# Oncilla Simulation Wizard
#
import os
import sys
from optparse import OptionParser
from wizard_helpers import *

tmpldir = '/tmp/oncwzrdtmpl'
tmplgitdir = '/tmp/oncwzrdgit'

def create_project(path):
    print 'Creating new Oncilla Simulation Webots Project at > '+path
    # Check if path is empty, then use / create
    if not check_if_project_folder_empty(path):
        print 'Could not create project folder'
        return False
        
    provide_project_template(tmpldir)
    
    # Export template to new project folder
    export_template_to_new_project(tmpldir, path)
    
    # Checks?
    
    # Compile and stuff
    
    # Checks?
    
def update_project(path):
    print 'Updating Oncilla Simulation Webots Project at > '+path
    # Check, if path is indeed already a project
    if not check_for_project_folder(path):
        print 'Folder doesn`t seem to be a proper project folder'
    
    # Check for a clean liboncilla-webots repository for the project template
    provide_project_template(tmpldir)
    
    # Somehow diff/update the project
    
    # Checks?
         
def main():
    usage = "Usage: %prog [options] [create_project / update_project]"
    parser = OptionParser(usage)
    parser.add_option("-p", "--path", dest="path",
                      help="path / destination of the project")
    parser.add_option("-q", "--quiet",
                      action="store_true", dest="verbose")
    (options, args) = parser.parse_args()
    
    if len(args) != 1:
        parser.error("Incorrect number of arguments.")
    if options.path==None:
        parser.error("Please provide a project path.")
        
    if args[0]=="create_project":
        create_project(options.path)
    elif args[0]=="create_project":
        update_project(options.path)
    else:
        parser.error("Unknown argument. Use either 'create_project' or 'update_project'.")

if __name__ == '__main__':
  main()