class Graph:

    def __init__(self, file_path=None):
        self.edge_list = {}

        if file_path:
            self._load_from_file(file_path)

    def _load_from_file(self, file_path):
        with open(file_path, "r") as file:
            for line in file:
                line = line.strip()
                if not line:  # evitar líneas vacías
                    continue

                parts = line.split()
                if len(parts) != 2:
                    raise ValueError(f"Línea inválida: {line}")

                origin, dest = parts
                self.add_edge(origin, dest)

    def add_edge(self, origin, dest):
        """Agrega una arista no dirigida entre origin y dest."""
        self.edge_list.setdefault(origin, set()).add(dest)
        self.edge_list.setdefault(dest, set()).add(origin)

    def remove_edge(self, origin, dest, remove_isolated=False):
        """Elimina la arista. 
        Si remove_isolated=True, borra vértices que queden sin conexiones.
        """

        if origin not in self.edge_list or dest not in self.edge_list[origin]:
            return False  # no existía

        self.edge_list[origin].remove(dest)
        self.edge_list[dest].remove(origin)

        if remove_isolated:
            if not self.edge_list[origin]:
                del self.edge_list[origin]
            if not self.edge_list[dest]:
                del self.edge_list[dest]

        return True  # se eliminó correctamente
    
    def __str__(self):
        return "\n".join(f"{node}: {neighbors}" for node, neighbors in self.edge_list.items())

