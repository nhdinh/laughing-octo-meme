from aloe import *
import math


@step(r"Given I have the number (\d+)")
def given_i_have_the_number(self, number):
    world.number = int(number)


@step(r"When I compute its factorial")
def _compute(self):
    world.number = factorial(world.number)


@step(r"Then I see the number (\d+)")
def assert_expectation(self, expectation):
    expectation = int(expectation)
    assert world.number == expectation, "Got returned %d" % world.number


def factorial(number):
    return math.factorial(number)
