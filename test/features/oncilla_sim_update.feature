Feature: Update an existing project
  In order to work with the latest Oncilla Simulator
  As an AMARSi user
  I want to update an exising project

  Scenario: Update an outdated Oncilla project tree
    Given I have an existing Oncilla project tree
    Given the Oncilla project tree is outdated
    When I ask to update the project tree
    Then I should get an updated project tree

  Scenario: Update an up-to-date Oncilla project tree
    Given I have an existing Oncilla project tree
    Given the Oncilla project tree is up-to-date
    When I ask to update the project tree
    Then I should get a message "already up-to-date"

  Scenario: Update a customized Oncilla project tree
    Given I have an existing Oncilla project tree
    Given I made some modification to the project tree
    When I ask to update the project tree
    Then I should be asked if I want to continue
    When I say yes
    Then I should get an updated project tree
    Then I should be able to get a backup of my customization

  Scenario: Update an existing non-emty tree
    Given I have a non-empty tree
    When I ask to update the project tree
    Then I should get an error "not an Oncilla project tree"

  Scenario: Update a non existing tree
    Given I have a non existing tree
    When I ask to update the project tree
    Then I should get an error "not an Oncilla project tree"
    
  Scenario: Update a webots tree
    Given I have a webots project tree
    When I ask to update the project tree
    Then I should have a ready to use project tree


