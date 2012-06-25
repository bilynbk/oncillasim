# Oncilla Simulation Wizard
import os
import sys
import string
import shutil

from git import *

def check_if_project_folder_empty(path):
    if os.path.exists(path):
        exit('''The given folder is not empty. If it's already a simulation project, try calling 'update_project' instead.''')
        return False
    return True

def create_new_project_folder(path):
    try:
        os.makedirs(path)
    except OSError as e:
        if e.errno==17:
            exit('''  Error: The given folder is not empty. If it's already a simulation project, try calling 'update_project' instead.''')
            return False
        else:
            exit("  I/O error({0}): {1}".format(e.errno, e.strerror))
            return False
    return True

def provide_project_template(path):
    print '[provide_project_template]'
    
    # Check if template directory already existing
    if os.path.exists(path+'/liboncilla-webots'):
        print path+' already existing ...'
        # Try to treat as repository and update
        repo = Repo.init(path+'/liboncilla-webots')
        
        # This will have to trigger an update, but we leave it for now
        #exit("Not implemented. Update repository")
        
    else:
        os.makedirs(path+'/liboncilla-webots')
    
        # Make a blank checkout of liboncilla-webots
        print 'Cloning project template from liboncilla-webots ...'
        wrepo = Repo.init()
        wrepo.clone_from("https://anordman@redmine.amarsi-project.eu/git/liboncilla-webots.git",
                        path+'/liboncilla-webots')
        
        # Make a blank checkout of liboncilla for example 1
        print 'Cloning examples from liboncilla ...'
        orepo = Repo.init()
        orepo.clone_from("https://anordman@redmine.amarsi-project.eu/git/quaddrivers.git",
                        path+'/liboncilla', None, b="dev")
        
        # Make a blank checkout of cca-oncilla for examples 2-4
        print 'Cloning examples from cca-oncilla ...'
        crepo = Repo.init()
        crepo.clone_from("https://anordman@redmine.amarsi-project.eu/git/oncilla-cca.git",
                        path+'/cca-oncilla')
        

def check_for_project_folder(path):
    # Check if path is existing
    if not os.path.exists(path):
        exit('''The given folder does not exist. If you want to create a new simulation project, try calling 'create_project' instead.''')
    
    # Check for existing content
    if not os.path.exists(path+'plugins') or not os.path.exists(path+'worlds'):
        exit('''The given folder doesn't seem to contain a proper project yet. If you want to create a new simulation project, try calling 'create_project' instead.''')

    return True

def export_template_to_new_project(tmpl, path):
    
    # Export basic project structure
    shutil.copytree(tmpl+"/liboncilla-webots/webots-data",
                    path,
                    symlinks=False,
                    ignore=shutil.ignore_patterns('.git*'))
    
    examples = ['Example1', 'Example2', 'Example3', 'Example4']
    for folder in examples:
        if not os.path.exists(path+'/controllers/'+folder):
            os.makedirs(path+'/controllers/'+folder)
    
    # Copy and compile example 1
    shutil.copy(tmpl+"/liboncilla/examples/SimpleSineMovement.cpp",
                    path+'/controllers/'+examples[0]+'/'+examples[0]+'.cpp')
    
    # Create world files
    # We have to replace the controller in the world files
    fo = open(path+"/worlds/Oncilla.wbt", "r+")
    world_orig = fo.read()
    for controller in examples:
         world = change_webots_controller(world_orig, controller)
         fn = open(os.path.join(path+"/worlds", controller+".wbt"), "w+")
         fn.write(world)
         
def change_webots_controller(world_orig, controller):
    return string.replace(world_orig, "development_controller", controller)
