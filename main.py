import tkinter as tk
from tkinter import filedialog
from tkinter.scrolledtext import ScrolledText
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from graph import Graph
from infection import Infection


# redirect print to GUI
class PrintCapture:
    def __init__(self, textbox: ScrolledText):
        self.textbox = textbox

    def write(self, text):
        self.textbox.insert(tk.END, text)
        self.textbox.see(tk.END)

    def flush(self):
        self.textbox.delete('1.0' , tk.END)


# Main GUI
class PandemicGUI:

    def __init__(self, root):
        self.root = root
        self.root.title("Pandemic Simulation")

        self.graph = None
        self.infection = None
        self.file_path = None
        self.end_time = None
        self.pos = None   # networkx layout

        self.show_upload_screen()

    # Screen 1
    def show_upload_screen(self):
        self.clear()

        label = tk.Label(self.root, text="Upload graph file and enter end time", font=("Arial", 14))
        label.pack(pady=10)

        btn_file = tk.Button(self.root, text="Upload File", command=self.load_file)
        btn_file.pack(pady=5)

        self.label_file = tk.Label(self.root, text="No file selected")
        self.label_file.pack()

        tk.Label(self.root, text="Enter max time t:").pack()

        self.entry_t = tk.Entry(self.root)
        self.entry_t.pack()

        btn_continue = tk.Button(self.root, text="Continue", command=self.to_origin_screen)
        btn_continue.pack(pady=15)

    def load_file(self):
        self.file_path = filedialog.askopenfilename()
        if self.file_path:
            self.label_file.config(text=self.file_path)

    def to_origin_screen(self):
        if not self.file_path:
            return

        try:
            self.end_time = int(self.entry_t.get())
        except:
            return

        self.graph = Graph(self.file_path)
        self.show_origin_screen()

    # Screen 2
    def show_origin_screen(self):
        self.clear()

        label = tk.Label(self.root, text="Enter starting node", font=("Arial", 14))
        label.pack(pady=10)

        # Pre-render graph
        self.Gnx = nx.Graph()
        for node, neighbors in self.graph.edge_list.items():
            for n in neighbors:
                self.Gnx.add_edge(node, n)

        self.pos = nx.spring_layout(self.Gnx)

        fig = plt.Figure(figsize=(5, 4))
        self.ax = fig.add_subplot(111)
        nx.draw(self.Gnx, self.pos, ax=self.ax, with_labels=True, node_color="lightblue")

        self.canvas = FigureCanvasTkAgg(fig, master=self.root)
        self.canvas.get_tk_widget().pack()

        tk.Label(self.root, text="Available nodes:").pack()
        tk.Label(self.root, text=str(list(self.Gnx.nodes))).pack()

        tk.Label(self.root, text="Start node:").pack()
        self.entry_origin = tk.Entry(self.root)
        self.entry_origin.pack()

        btn_start = tk.Button(self.root, text="Start Simulation", command=self.start_simulation)
        btn_start.pack(pady=15)

    # Screen 3
    def start_simulation(self):
        origin = self.entry_origin.get()

        if origin not in self.Gnx.nodes:
            return

        self.infection = Infection(self.graph.edge_list, origin)

        self.show_simulation_screen()

    def show_simulation_screen(self):
        self.clear()

        title = tk.Label(self.root, text="Pandemic Simulation", font=("Arial", 16))
        title.pack(pady=10)

        # graph display area
        fig = plt.Figure(figsize=(6, 4))
        self.ax = fig.add_subplot(111)

        self.canvas = FigureCanvasTkAgg(fig, master=self.root)
        self.canvas.get_tk_widget().pack()

        # log box
        tk.Label(self.root, text="Simulation Log:").pack()
        self.log_box = ScrolledText(self.root, width=70, height=10)
        self.log_box.pack(pady=5)

        self.print_capture = PrintCapture(self.log_box)
        # redirect print
        import sys
        sys.stdout = self.print_capture

        # status labels
        self.info_label = tk.Label(self.root, text="")
        self.info_label.pack(pady=5)

        # Buttons
        self.btn_next = tk.Button(self.root, text="Next t", command=self.next_step)
        self.btn_next.pack(pady=10)

        # First draw (t=0)
        self.draw_graph()

    # Draw graph colored by infection state
    def draw_graph(self):
        infected = self.infection.infected

        node_colors = [
            "red" if node in infected else "green"
            for node in self.Gnx.nodes
        ]

        self.ax.clear()
        nx.draw(
            self.Gnx,
            self.pos,
            ax=self.ax,
            with_labels=True,
            node_color=node_colors,
            edge_color="gray"
        )
        self.canvas.draw()

    # Advance simulation by one timestep
    def next_step(self):
        if self.infection.t > self.end_time:
            self.btn_next.config(state=tk.DISABLED)
            return

        newly = self.infection.update()
        healthy = self.infection.get_healthy_vertices()

        self.draw_graph()

        self.info_label.config(
            text=f"t={self.infection.t} | Newly infected: {newly} | "
                 f"Infected: {len(self.infection.infected)} | Healthy: {len(healthy)}"
        )

        # End conditions
        if newly == 0 or len(healthy) == 0:
            self.btn_next.config(state=tk.DISABLED)

    # Utility: clear window
    def clear(self):
        for widget in self.root.winfo_children():
            widget.destroy()


# ---------------- RUN APP ----------------
if __name__ == "__main__":
    root = tk.Tk()
    app = PandemicGUI(root)
    root.mainloop()
