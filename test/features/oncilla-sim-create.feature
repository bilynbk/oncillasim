Feature: Create a new project
  In order to work with Oncilla Simulator
  As an amarsi user
  I would like to create a new project

  Scenario: Create a new project in an empty directory
    Given I have an empty path
    When I ask to create a new oncilla project
    Then I should have a ready to use project in that path

  Scenario: Create a new project in an non-empty directory
    Given I have a non-empty path
    When I ask to create a new oncilla project
    Then I should get an error

  Scenario: Create a new project in an already existing project
    Given I have an existing project path
    When I ask to create a new oncilla porject
    Then I should get an error

