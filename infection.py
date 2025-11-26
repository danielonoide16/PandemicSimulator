import random
import networkx as nx

class Infection:

    def __init__(self, graph: nx.Graph, start_node):
        self.graph = graph
        self.t = 0

        self.infected = {start_node}   # all infected


    def update(self):
        """
        one timestep of infection.
        """

        newly_infected_count = 0
        infectors = self.infected.copy()

        for node in infectors:
            print("\nNode ", node, " is infecting...")

            if len([n for n in self.graph.neighbors(node) if n not in self.infected]) == 0: #si no tiene nodos para infectar
                print("No neighbors to infect\n")
                continue


            for neighbor in self.graph.neighbors(node):

                if neighbor in self.infected:
                    print(neighbor, " is already infected")
                    continue  
                
                # infection attempt
                if random.random() >= 0.5:
                    self.infected.add(neighbor)
                    newly_infected_count += 1
                    print(neighbor, " was infected")
                else:
                    print(neighbor, " was not infected")

        self.t += 1

        return newly_infected_count


    def get_healthy_vertices(self):
        return set(self.graph.nodes()) - self.infected
