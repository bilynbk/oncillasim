# -*- coding: utf-8 -*-
import os
import sys

from lettuce import *

from oncilla_wizard import *

################################################################################
# Given
################################################################################

@step(u'Given I have a non existing tree ([\w\/]+)')
def given_i_have_a_non_existing_tree(step, path):
    world.path = path

@step(u'Given I have a non-empty tree')
def given_i_have_a_non_empty_tree(step):
    world.path = '.'

@step(u'Given I have a Webots project tree')
def given_i_have_an_existing_webots_project_tree(step):
    assert False, 'This step must be implemented'

@step(u'Given I have an existing Oncilla project tree')
def given_i_have_an_existing_oncilla_project_tree(step):
    assert False, 'This step must be implemented'

@step(u'Given the Oncilla project tree is outdated')
def given_the_oncilla_project_tree_is_outdated(step):
    assert False, 'This step must be implemented'

@step(u'Given the Oncilla project tree is up-to-date')
def given_the_oncilla_project_tree_is_up_to_date(step):
    assert False, 'This step must be implemented'

@step(u'Given I made some modification to the project tree')
def given_i_made_some_modification_to_the_project_tree(step):
    assert False, 'This step must be implemented'


################################################################################
# When
################################################################################

@step(u'When I ask to create the project tree')
def when_i_ask_to_create_the_project_tree(step):
    create_project(world.path)

@step(u'When I ask to update the project tree')
def when_i_ask_to_update_the_project_tree(step):
    update_project(world.path)

@step(u'When I say yes')
def when_i_say_yes(step):
    assert False, 'This step must be implemented'

################################################################################
# Then
################################################################################

@step(u'Then I should have a ready to use project tree')
def then_i_should_have_a_ready_to_use_project_tree(step):
    assert os.path.exists(os.path.abspath(world.path + '/worlds'))
    assert os.path.exists(os.path.abspath(world.path + '/plugins'))

@step(u'Then I should get an error "([^"]*)"')
def then_i_should_get_an_error_group1(step, group1):
    assert False, 'This step must be implemented'

@step(u'Then I should get an updated project tree')
def then_i_should_get_an_updated_project_tree(step):
    assert False, 'This step must be implemented'

@step(u'Then I should get a message "([^"]*)"')
def then_i_should_get_a_message_group1(step, group1):
    assert False, 'This step must be implemented'

@step(u'Then I should be asked if I want to continue')
def then_i_should_be_asked_if_i_want_to_continue(step):
    assert False, 'This step must be implemented'

@step(u'Then I should be able to get a backup of my customization')
def then_i_should_be_able_to_get_a_backup_of_my_customization(step):
    assert False, 'This step must be implemented'
