import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.scrolledtext import ScrolledText
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from infection import Infection


# redirect print to GUI
class PrintCapture:
    def __init__(self, textbox: ScrolledText):
        self.textbox = textbox
        self.textbox.config(state=tk.DISABLED)

    def write(self, text):
        self.textbox.config(state=tk.NORMAL)
        self.textbox.insert(tk.END, text)
        self.textbox.see(tk.END)
        self.textbox.config(state=tk.DISABLED)

    def flush(self):
        self.textbox.config(state=tk.NORMAL)
        self.textbox.delete("1.0", tk.END)
        self.textbox.config(state=tk.DISABLED)


# Main GUI
class Pandemic:

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

        btn_file = tk.Button(self.root, text="Upload file", command=self.load_file)
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
            messagebox.showerror("ERROR", "No input file selected")
            return

        try:
            self.end_time = int(self.entry_t.get())
            self.graph = nx.read_edgelist(self.file_path, create_using=nx.Graph())
        except TypeError:
            messagebox.showerror("ERROR", "Incorrect file format")
            return
        except:
            messagebox.showerror("ERROR", "Incorrect time format")
            return


        self.show_origin_screen()

    # Screen 2
    def show_origin_screen(self):
        self.clear()

        label = tk.Label(self.root, text="Enter starting node", font=("Arial", 14))
        label.pack(pady=10)

        self.pos = nx.spring_layout(self.graph)

        fig = plt.Figure(figsize=(7, 5))
        self.ax = fig.add_subplot(111) #rows, cols, index
        nx.draw(self.graph, self.pos, ax=self.ax, with_labels=True, node_color="lightblue")

        #interfaz entre tkinter y matplotlib
        self.canvas = FigureCanvasTkAgg(fig, master=self.root)
        self.canvas.get_tk_widget().pack()

        tk.Label(self.root, text="Available nodes:").pack()
        tk.Label(self.root, text=str(list(self.graph.nodes))).pack()

        tk.Label(self.root, text="Start node:").pack()
        self.entry_origin = tk.Entry(self.root)
        self.entry_origin.pack()

        btn_start = tk.Button(self.root, text="Start Simulation", command=self.start_simulation)
        btn_start.pack(pady=15)

    # Screen 3
    def start_simulation(self):
        origin = self.entry_origin.get()

        if origin not in self.graph.nodes:
            messagebox.showerror("ERROR", "Node not found")
            return

        self.infection = Infection(self.graph, origin)

        self.show_simulation_screen()

    def show_simulation_screen(self):
        self.clear()

        title = tk.Label(self.root, text="Pandemic Simulation", font=("Arial", 16))
        title.pack(pady=10)

        tk.Button(self.root, text="Restart", command=self.show_upload_screen).pack()

        # graph display area
        fig = plt.Figure(figsize=(6, 4))
        self.ax = fig.add_subplot(111)

        self.canvas = FigureCanvasTkAgg(fig, master=self.root)
        self.canvas.get_tk_widget().pack()

        # log box
        tk.Label(self.root, text="Log:").pack()
        self.log_box = ScrolledText(self.root, width=70, height=10)
        self.log_box.pack(pady=5)

        self.print_capture = PrintCapture(self.log_box)
        # redirect print
        import sys
        sys.stdout = self.print_capture

        tk.Button(self.root, text="Flush log", command=self.print_capture.flush).pack()

        # status labels
        self.info_label = tk.Label(self.root, text="")
        self.info_label.pack(pady=5)

        # buttons
        self.btn_next = tk.Button(self.root, text="Next t", command=self.next_step)
        self.btn_next.pack(pady=10)

        # first draw (t=0)
        self.draw_graph()

    # Draw graph colored by infection state
    def draw_graph(self):
        infected = self.infection.infected

        node_colors = [
            "salmon" if node in infected else "springgreen"
            for node in self.graph.nodes
        ]

        self.ax.clear()
        nx.draw(
            self.graph,
            self.pos,
            ax=self.ax,
            with_labels=True,
            node_color=node_colors,
            edge_color="gray"
        )
        self.canvas.draw()

    # move the simulation by one timestep
    def next_step(self):
        if self.infection.t >= self.end_time:
            self.btn_next.config(state=tk.DISABLED)
            messagebox.showinfo("End", "The time limit has been reached")
            return
        

        print("----- Time t =", self.infection.t + 1, " -----")

        newly = self.infection.update()
        healthy = self.infection.get_healthy_vertices()

        self.draw_graph()

        self.info_label.config(
            text=f"t={self.infection.t} | Newly infected: {newly} | "
                 f"Infected: {len(self.infection.infected)} | Healthy: {len(healthy)}"
        )

        #end conditions
        if newly == 0 or len(healthy) == 0:
            self.btn_next.config(state=tk.DISABLED)
            messagebox.showinfo("End", "No more infections possible")
            

    #clear window
    def clear(self):
        for widget in self.root.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = Pandemic(root)
    root.mainloop()
