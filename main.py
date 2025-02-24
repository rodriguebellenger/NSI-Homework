import tkinter as tk
from tkinter import messagebox

class LogicGate:
    def __init__(self, app, canvas, x, y, gate_type):
        self.app = app  # Référence à l'application principale
        self.canvas = canvas
        self.x = x
        self.y = y
        self.gate_type = gate_type
        self.inputs = []  # List of connected input gates
        self.output = 0
        self.connections = []
        self.lines = []
        self.draw_gate()
        self.bind_drag()
        self.bind_connect()
        self.bind_delete_connections()
    
    def draw_gate(self):
        self.rect = self.canvas.create_rectangle(self.x, self.y, self.x+50, self.y+50, fill="lightgray", tags="gate")
        self.text = self.canvas.create_text(self.x+25, self.y+25, text=self.gate_type, tags="gate")
        self.update_output()
    
    def update_output(self):
        input_values = [gate.output for gate in self.inputs]
        if self.gate_type == "AND":
            self.output = int(len(input_values) == 2 and all(input_values))
        elif self.gate_type == "OR":
            self.output = int(len(input_values) == 2 and any(input_values))
        elif self.gate_type == "NOT":
            self.output = int(len(input_values) == 1 and not input_values[0])
        self.canvas.itemconfig(self.text, text=f"{self.gate_type}\n{self.output}")
        self.update_connections()
    
    def bind_drag(self):
        self.canvas.tag_bind(self.rect, "<ButtonPress-1>", self.on_start)
        self.canvas.tag_bind(self.text, "<ButtonPress-1>", self.on_start)
        self.canvas.tag_bind(self.rect, "<B1-Motion>", self.on_drag)
        self.canvas.tag_bind(self.text, "<B1-Motion>", self.on_drag)
    
    def bind_connect(self):
        self.canvas.tag_bind(self.rect, "<ButtonPress-3>", self.on_select)
        self.canvas.tag_bind(self.text, "<ButtonPress-3>", self.on_select)
    
    def bind_delete_connections(self):
        self.canvas.tag_bind(self.rect, "<Double-Button-1>", self.on_delete_connections)
        self.canvas.tag_bind(self.text, "<Double-Button-1>", self.on_delete_connections)
    
    def on_start(self, event):
        self.start_x = event.x
        self.start_y = event.y
    
    def on_drag(self, event):
        dx = event.x - self.start_x
        dy = event.y - self.start_y
        self.canvas.move(self.rect, dx, dy)
        self.canvas.move(self.text, dx, dy)
        self.x += dx
        self.y += dy
        self.start_x = event.x
        self.start_y = event.y
        self.update_connections()
        self.app.update_all_connections()
    
    def on_select(self, event):
        self.app.select_gate(self)
    
    def on_delete_connections(self, event):
        self.inputs.clear()
        self.connections.clear()
        self.update_connections()
    
    def connect_to(self, other_gate):
        if len(other_gate.inputs) < (2 if other_gate.gate_type in ["AND", "OR"] else 1):
            other_gate.inputs.append(self)
            self.connections.append(other_gate)
            self.app.update_all_connections()
    
    def update_connections(self):
        for line in self.lines:
            self.canvas.delete(line)
        self.lines.clear()
        for gate in self.connections:
            line = self.canvas.create_line(self.x+50, self.y+25, gate.x, gate.y+25, arrow=tk.LAST, tags="connections")
            self.lines.append(line)

class Switch:
    def __init__(self, app, canvas, x, y):
        self.app = app
        self.canvas = canvas
        self.x = x
        self.y = y
        self.state = 0
        self.connections = []
        self.draw_switch()
    
    def draw_switch(self):
        self.rect = self.canvas.create_rectangle(self.x, self.y, self.x+50, self.y+50, fill="yellow", tags="switch")
        self.text = self.canvas.create_text(self.x+25, self.y+25, text=str(self.state), tags="switch")
        self.canvas.tag_bind(self.rect, "<Button-1>", self.toggle)
        self.canvas.tag_bind(self.text, "<Button-1>", self.toggle)
    
    def toggle(self, event):
        self.state = 1 - self.state
        self.canvas.itemconfig(self.text, text=str(self.state))
        self.update_connections()
    
    def connect_to(self, gate):
        if len(gate.inputs) < (2 if gate.gate_type in ["AND", "OR"] else 1):
            gate.inputs.append(self)
            self.connections.append(gate)
            self.app.update_all_connections()
    
    def update_connections(self):
        for gate in self.connections:
            gate.update_output()

class LogicCircuitApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Logic Circuit Simulator")
        self.canvas = tk.Canvas(root, width=500, height=400, bg="white")
        self.canvas.pack()
        
        self.gates = []
        self.selected_gate = None
        self.add_buttons()
    
    def add_buttons(self):
        frame = tk.Frame(self.root)
        frame.pack()
        
        tk.Button(frame, text="Add AND Gate", command=lambda: self.add_gate("AND")).pack(side=tk.LEFT)
        tk.Button(frame, text="Add OR Gate", command=lambda: self.add_gate("OR")).pack(side=tk.LEFT)
        tk.Button(frame, text="Add NOT Gate", command=lambda: self.add_gate("NOT")).pack(side=tk.LEFT)
        tk.Button(frame, text="Add Switch", command=self.add_switch).pack(side=tk.LEFT)
        tk.Button(frame, text="Run Simulation", command=self.run_simulation).pack(side=tk.LEFT)
        tk.Button(frame, text="Reset Circuit", command=self.reset_circuit).pack(side=tk.LEFT)
    
    def add_gate(self, gate_type):
        gate = LogicGate(self, self.canvas, 50, 100, gate_type)
        self.gates.append(gate)
    
    def add_switch(self):
        switch = Switch(self, self.canvas, 50, 100)
        self.gates.append(switch)
    
    def reset_circuit(self):
        self.canvas.delete("all")
        self.gates.clear()
        self.selected_gate = None

if __name__ == "__main__":
    root = tk.Tk()
    app = LogicCircuitApp(root)
    root.mainloop()
