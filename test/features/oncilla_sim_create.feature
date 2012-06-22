Feature: Create a new project
  In order to work with Oncilla Simulator
  As an AMARSi user
  I would like to create a new project

  Scenario: Create a new Oncilla project in a non existing
    Given I have a non existing tree /tmp/nonexisting
    When I ask to create the project tree
    Then I should have a ready to use project tree

  Scenario: Create a new Oncilla project in an non-empty tree
    Given I have a non-empty tree
    When I ask to create the project tree
    Then I should get an error "non empty"

  Scenario: Create a new Oncilla project in an already existing Oncilla tree
    Given I have an existing Oncilla project tree
    When I ask to create the project tree
    Then I should get an error "update needed"

  Scenario: Create a new Oncilla project in an already existing Webots tree
    Given I have a Webots project tree
    When I ask to create the project tree
    Then I should have a ready to use project tree
