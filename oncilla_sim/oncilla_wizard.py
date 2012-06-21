# Oncilla Simulation Wizard
import os
import sys

from wizard_helpers import *

tmpldir = '/tmp/oncwzrd'

def create_project(path):
    print 'Creating new Oncilla Simulation Webots Project at > '+path
    # Check if path is empty, then use / create
    create_new_project_folder(path)
    
    # Check for a clean liboncilla-webots repository for the project template
    provide_project_template(tmpldir)
    
    # Export template to new project folder
    export_template_to_new_project(tmpldir)
    
    # Checks?
    
    # Compile and stuff
    
    # Checks?
    
def update_project(path):
    print 'Updating Oncilla Simulation Webots Project at > '+path
    # Check, if path is indeed already a project
    check_for_project_folder(path)
    
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
