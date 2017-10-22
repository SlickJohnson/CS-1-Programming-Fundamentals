import random
import sys

from virus import Virus
from person import Person
from logger import Logger

random.seed(42)


class Simulation(object):

    def __init__(self, population_size, vacc_percentage, virus_name,
                 mortality_rate, basic_repro_num, initial_infected=1):
        self.population_size = population_size
        self.total_infected = initial_infected
        self.current_infected = initial_infected
        self.next_person_id = 0
        self.virus = Virus(virus_name, mortality_rate, basic_repro_num)
        self.file_name = "{}_simulation_pop_{}_vp_{}_infected_{}.txt".format(
            virus_name, population_size, vacc_percentage, initial_infected)

        self.logger = Logger(self.file_name)
        self.logger.write_metadata(population_size, vacc_percentage, virus_name, mortality_rate, basic_repro_num)

        self.newly_infected = []

        self.population = self._create_population()

    def _create_population(self):
        population = []
        infected_count = 0
        while len(population) < population_size:
            person = Person(self.next_person_id, False)

            if infected_count != initial_infected:
                person.infected = True
                person.infection = self.virus

                infected_count += 1
            else:
                if random.random() < vacc_percentage:
                    person.is_vaccinated = True

            population.append(person)
            self.next_person_id += 1

        return population

    def _simulation_should_continue(self):
        if len(self.population) == 0:
            return False

        if self.current_infected == 0:
            return False

        return True

    def run(self):
        time_step_counter = 0
        should_continue = self._simulation_should_continue()

        while should_continue:
            self.time_step()
            should_continue = self._simulation_should_continue()

        print('The simulation has ended after {} turns.'.format(time_step_counter))

    def time_step(self):
        for person in self.population:
            if not person.is_infected:
                continue

            interaction_counter = 0
            while interaction_counter != 100:
                random_person = self.population[random.randint(0, self.population_size)]

                if not random_person.is_alive:
                    continue

                self.interaction(person, random_person)
                interaction_counter += 1

        self._infect_newly_infected()

    def interaction(self, person1, person2):
        assert person1.is_alive
        assert person2.is_alive

        if person2.is_vaccinated:
            self.logger.log_interaction(person1, person2, False, person2.is_vaccinated, person2.is_infected)
            return

        if person2.is_infected:
            self.logger.log_interaction(person1, person2, False, person2.is_vaccinated, person2.is_infected)
            return

        if random.random() < person1.infection.basic_repo_num:
            self.newly_infected.append(person2.get_person_id())
            self.logger.log_interaction(person1, person2, True, person2.is_vaccinated, person2.is_infected)

    def _infect_newly_infected(self):
        for person in self.population:
            if not person.get_person_id() in self.newly_infected:
                continue

            person.is_infected = True
            person.infected = self.virus
            person.did_survive_infection()
            self.current_infected -= 1

        self.newly_infected = []


if __name__ == "__main__":
    params = sys.argv[1:]
    population_size = int(params[0])
    vacc_percentage = float(params[1])
    virus_name = str(params[2])
    mortality_rate = float(params[3])
    basic_repro_num = float(params[4])
    if len(params) == 6:
        initial_infected = int(params[5])
    else:
        initial_infected = 1
    simulation = Simulation(population_size, vacc_percentage, virus_name, mortality_rate,
                            basic_repro_num, initial_infected)
    simulation.run()
