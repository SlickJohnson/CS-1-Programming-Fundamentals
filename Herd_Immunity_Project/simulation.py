import random
import sys

from virus import Virus
from person import Person
from logger import Logger

random.seed(42)


class Simulation(object):

    def __init__(self, population_size, vacc_percentage, virus_name,
                 mortality_rate, basic_repro_num, initial_infected=1):
        print("Initializing simulation...")

        # Virus
        self.virus_name = virus_name
        self.mortality_rate = mortality_rate
        self.basic_repro_num = basic_repro_num
        self.virus = Virus(virus_name, mortality_rate, basic_repro_num)
        # Population
        self.vacc_percentage = vacc_percentage
        self.population_size = population_size
        self.initial_infected = initial_infected
        self.total_infected = initial_infected
        self.current_infected = initial_infected
        # Logger
        self.file_name = "{}_simulation_pop_{}_vp_{}_infected_{}.txt".format(
            virus_name, population_size, vacc_percentage, initial_infected)
        self.logger = Logger(self.file_name)
        self.logger.write_metadata(population_size, vacc_percentage, virus_name, mortality_rate, basic_repro_num)
        # Simulation
        self.next_person_id = 0
        self.newly_infected = []
        self.population = self._create_population()
        self.current_population_size = population_size

    def _create_population(self):
        print("Creating Humans for simulation...")
        new_population = []
        infected_count = 0
        while len(new_population) < self.population_size:
            person = Person(self.next_person_id, False)

            if infected_count != self.initial_infected:
                person.is_infected = True
                person.infection = self.virus

                infected_count += 1
                print("Created Infected Human")
            else:
                if random.random() < self.vacc_percentage:
                    print("Created Vaccinated Human")
                    person.is_vaccinated = True

            new_population.append(person)
            self.next_person_id += 1
        print("All Humans Created...")
        return new_population

    def _simulation_should_continue(self):
        print("Current Population Size:  {}\tCurret Infected:  {}".format(self.current_population_size, self.current_infected))
        if self.current_population_size == 0 or self.current_infected == 0:
            print("Contine? False")
            return False
        print("Contine? True")
        return True

    def run(self):
        print("Running simulation.......")
        time_step_counter = 0
        should_continue = True

        while should_continue:
            self.time_step()
            time_step_counter += 1
            should_continue = self._simulation_should_continue()
            print("Time Step Counter", should_continue)

        print("Time step counter: ", time_step_counter)
        print('The simulation has ended after {} turns.'.format(time_step_counter))

    def time_step(self):
        for person in self.population:
            # print("Found a person... Checking to see if infected...")
            if person.is_infected:
                interaction_counter = 0
                while interaction_counter < 100:
                    # print("Humans Interact")
                    random_person = self.population[random.randint(0, self.population_size - 1)]

                    if random_person.is_alive and person.is_alive:
                        self.interaction(person, random_person)
                        interaction_counter += 1
                        print("INTERACT. Interaction counter is now:", interaction_counter, person)

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

        if random.random() < self.basic_repro_num:
            self.newly_infected.append(person2.get_person_id())
            self.current_infected += 1
            self.logger.log_interaction(person1, person2, True, person2.is_vaccinated, person2.is_infected)

    def _infect_newly_infected(self):
        print("Checking Survivers")
        for person in self.population:
            if person.get_person_id() in self.newly_infected:
                print("I'M INFECTED!!!NOOOOO")
                person.is_infected = True
                person.infection = self.virus
                print("Person Infected With Virus: ", person.infection)

                if not person.did_survive_infection():
                    self.current_population_size -= 1

                self.current_infected -= 1
                print("Currently infected people...:", self.current_infected)
        print("Get new newly_infected list")
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
