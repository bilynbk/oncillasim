#!/usr/bin/env python
#
# Oncilla Simulation Wizard
#
import os
import sys
from argparse import ArgumentParser
from wizard_helpers import *

tmpldir = '/tmp/oncwzrdtmpl'
tmplgitdir = '/tmp/oncwzrdgit'

def create_project(path):
    print 'Creating new Oncilla Simulation Webots Project at > '+path
    # Check if path is empty, then use / create
    if not check_if_project_folder_empty(path):
        exit('Could not create project folder')
        
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
    usage = "Usage: %prog [options] (create_project / update_project) path"
    parser = ArgumentParser()
    parser.add_argument("-q", "--quiet", action='count', help="be quiet")
    parser.add_argument("command", help="command, either 'create' or 'update'")
    parser.add_argument("path", help="path / destination of the project")
    args = parser.parse_args()
    
    if args.command == "create":
        create_project(args.path)
    elif args.command == "update":
        update_project(args.path)
    else:
        parser.error("Unknown argument. Use either 'create_project' or 'update_project'.")

if __name__ == '__main__':
    main()
