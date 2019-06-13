Feature: Compute factorial
  In order to play with Lettuce
  As a beginners
  We'll implement factorial

  Scenario: Factorial of 0
    Given I have the number 0
    When I compute its factorial
    Then I see the number 1

  Scenario: Factorial of 1
    Given I have the number 1
    When I compute its factorial
    Then I see the number 1

  Scenario: Factorial of 10
    Given I have the number 10
    When I compute its factorial
    Then I see the number 3628800