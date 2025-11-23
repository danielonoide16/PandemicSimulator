import random

class Infection:

    def __init__(self, edge_list: dict, start_node):
        self.graph = edge_list
        self.t = 0

        self.infected = {start_node}   # all infected
        self.currently_infected = {start_node}   # infected at the current time step


    def update(self):
        """
        one timestep of infection.
        """

        if not self.currently_infected:
            return 0  # no one left to spread infection

        new_currently_infected = set()
        newly_infected_count = 0

        for node in self.currently_infected:
            neighbors = self.graph.get(node, [])

            print("Node ", node, " is infecting...")

            for neighbor in neighbors:

                if neighbor in self.infected:
                    print(neighbor, " is already infected")
                    continue  # already infected earlier
                
                # infection attempt
                if random.random() >= 0.5:
                    self.infected.add(neighbor)
                    new_currently_infected.add(neighbor) 
                    newly_infected_count += 1
                    print(neighbor, " was infected")
                else:
                    print(neighbor, " was not infected")

        # prepare for next timestep
        self.currently_infected = new_currently_infected
        self.t += 1

        return newly_infected_count


    def get_healthy_vertices(self):
        return set(self.graph.keys()) - self.infected
