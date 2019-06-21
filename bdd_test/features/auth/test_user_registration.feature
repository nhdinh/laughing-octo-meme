Feature: Test user registration
	Scenario: New Registration
		Given I have username the_user with password P@ssW0rd!
		When I request the resource '/api/v1/users' with POST method
		Then I should see return 201 code
		
	Scenario: Registration with simple password
		Given I have username the_another_user with password password
		When I request the resource '/api/v1/users' with POST method
		Then I should see return 400 code

	Scenario: Registration with no data provided
		When I request the resource '/api/v1/users' with POST method
		Then I should see return 400 code
		And I should see return message 'No input data provided'

	Scenario: Duplicated registration
		Given I have username the_user with password Anoth3rP@ssW0rd!
		When I request the resource '/api/v1/users' with POST method
		And I request the resource '/api/v1/users' with POST method
		Then I should see return 400 code
		And I should see return message 'An user with the same name already exists'