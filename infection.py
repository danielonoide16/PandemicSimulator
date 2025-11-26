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

            healthy_neighbors = [n for n in self.graph.neighbors(node) if n not in self.infected]

            if not healthy_neighbors:
                print(node, " has no neighbors to infect")
                continue


            for neighbor in healthy_neighbors:
                # infection attempt
                if random.random() >= 0.5:
                    self.infected.add(neighbor)
                    newly_infected_count += 1
                    print(neighbor, "was infected by", node)
                else:
                    print(neighbor, "was NOT infected by", node)

        self.t += 1

        return newly_infected_count


    def get_healthy_vertices(self):
        return set(self.graph.nodes()) - self.infected
