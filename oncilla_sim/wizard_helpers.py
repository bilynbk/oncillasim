# Oncilla Simulation Wizard
import os
import sys

def create_new_project_folder(path):
    try:
        os.mkdir(path)
    except OSError as e:
        if e.errno==17:
            print '''  Error: The given folder is not empty. If it's already a
                proper simulation project, try calling 'update_project' instead.'''
        else:
            print "I/O error({0}): {1}".format(e.errno, e.strerror)

def check_for_project_folder(path):
    # Check if path is existing
    # Check for some features (contained files/folders)
    print ""

def provide_project_template(path):
    print ""

def export_template_to_new_project(path):
    print ""

def provide_project_template(path):
    print ""

def print_help():
    print '''Usage:
    python oncilla_wizard.py [create_project update_project] path
    
create_project    Will create a completely new project from scratch, with
                  examples included.
    
update_project    Will update an already existing project.
'''
    exit()
