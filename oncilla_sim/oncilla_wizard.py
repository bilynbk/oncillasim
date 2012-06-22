# Oncilla Simulation Wizard
import os
import sys

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

if len(sys.argv) < 3:
    # Help
    print_help()

if sys.argv[1] == "create_project":
    # Create new project
    create_project(sys.argv[2])
elif sys.argv[1] == "update_project":
    # Update existing project
    update_project(sys.argv[2])
else:
    # Help
    print_help()
