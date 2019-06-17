Feature: Test application

  Scenario: Test application when unauthorized
    Given I am unauthorized user
    When I request the resource '/' with GET method
    Then I should see the 401 message

  Scenario: Test application when authorized
    Given I am authorized user
    When I request the resource '/' with GET method
    Then I should see the 200 message

  Scenario: Test categories endpoint when authorized
    Given I am authorized user
    When I request the resource '/api/v1/categories' with GET method
    Then I should see the 200 message