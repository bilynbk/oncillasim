# Oncilla Simulation Wizard
import os
import sys
import shutil

from git import *

def check_if_project_folder_empty(path):
    if os.path.exists(path):
        print '''  Error: The given folder is not empty. If it's already a
  simulation project, try calling 'update_project' instead.'''
        return False
    return True

def create_new_project_folder(path):
    try:
        os.makedirs(path)
    except OSError as e:
        if e.errno==17:
            print '''  Error: The given folder is not empty. If it's already a
  simulation project, try calling 'update_project' instead.'''
            return False
        else:
            print "  I/O error({0}): {1}".format(e.errno, e.strerror)
            return False
    return True

def provide_project_template(path):
    print '[provide_project_template]'
    
    # Check if template directory already existing
    if os.path.exists(path+'/liboncilla-webots'):
        print path+' already existing ...'
        # Try to treat as repository and update
        repo = Repo.init(path+'/liboncilla-webots')
        
        print "Not implemented. Update repository"
        exit()
        
    else:
        os.makedirs(path+'/liboncilla-webots')
    
        # Make a blank checkout of liboncilla-webots
        print 'Cloning project template from liboncilla-webots ...'
        repo = Repo.init()
        repo.clone_from("https://anordman@redmine.amarsi-project.eu/git/liboncilla-webots.git",
                        path+'/liboncilla-webots')
        
        # Make a blank checkout of liboncilla for example 1
        print 'Cloning project template from liboncilla ...'
        repo = Repo.init()
        repo.clone_from("https://anordman@redmine.amarsi-project.eu/git/quaddrivers.git",
                        path+'/liboncilla')
        
        # Make a blank checkout of cca-oncilla for examples 2-4
        print 'Cloning project template from cca-oncilla ...'
        repo = Repo.init()
        repo.clone_from("https://anordman@redmine.amarsi-project.eu/git/quaddrivers.git",
                        path+'/cca-oncilla')
        

def check_for_project_folder(path):
    # Check if path is existing
    if not os.path.exists(path):
        print '''  Error: The given folder does not exist. If you want to create
  a new simulation project, try calling 'create_project' instead.'''
        return False
    
    # Check for existing content
    if not os.path.exists(path+'plugins') or not os.path.exists(path+'worlds'):
        print '''  Error: The given folder doesn't seem to contain a proper
  project yet. If you want to create a new simulation project, try calling
  'create_project' instead.'''
        return False

    return True

def export_template_to_new_project(tmpl, path):
    
    # Export basic project structure
    shutil.copytree(tmpl+"/liboncilla-webots/webots-data",
                    path,
                    symlinks=False,
                    ignore=shutil.ignore_patterns('.git*'))
    
    # If not already existing, create controllers folder
    if not os.path.exists(path+'/controllers'):
        os.mkdir(path+'/controllers')
        
    # Copy example 1
    shutil.copytree(tmpl+"/liboncilla/examples/SimpleSineMovement.cpp",
                    path+'/controllers',
                    symlinks=False,
                    ignore=shutil.ignore_patterns('.git*'))

def print_help():
    print '''Usage:
    python oncilla_wizard.py [create_project update_project] path
    
create_project    Will create a completely new project from scratch, with
                  examples included.
    
update_project    Will update an already existing project.
'''
    exit()
