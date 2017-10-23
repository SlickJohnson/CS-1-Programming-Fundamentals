from person import Person
from virus import Virus
import pytest


def setup_for_test():
    person = Person(1, False)
    return person


def test_init_person():
    person = setup_for_test()

    assert person.get_person_id() == 1
    assert person.is_infected is False


def test_infect_person():
    person = setup_for_test()

    person.infection = Virus("Ebola", -2, 0.25)
    assert person.infection.name == "Ebola"
    assert person.did_survive_infection() is True

    person.infection = Virus("Ebola", 2, 0.25)
    assert person.did_survive_infection() is False

