import tkinter as tk

class LogicGate:
    def __init__(self, app, canvas, x, y, gate_type):
        self.app = app
        self.canvas = canvas
        self.x = x
        self.y = y
        self.gate_type = gate_type
        self.inputs = []
        self.output = 0
        self.connections = []
        self.lines = []
        self.draw_gate()
        self.bind_events()
    
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
        self.app.mark_for_update(self)  # Mark gate for update instead of calling update_all_connections directly
    
    def bind_events(self):
        self.canvas.tag_bind(self.rect, "<ButtonPress-1>", self.on_start)
        self.canvas.tag_bind(self.text, "<ButtonPress-1>", self.on_start)
        self.canvas.tag_bind(self.rect, "<B1-Motion>", self.on_drag)
        self.canvas.tag_bind(self.text, "<B1-Motion>", self.on_drag)
        self.canvas.tag_bind(self.rect, "<ButtonPress-3>", self.on_select)
        self.canvas.tag_bind(self.text, "<ButtonPress-3>", self.on_select)
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
        self.app.update_all_connections()
    
    def on_select(self, event):
        self.app.select_gate(self)
    
    def on_delete_connections(self, event):
        self.inputs.clear()
        self.connections.clear()
        self.app.update_all_connections()
    
    def connect_to(self, other_gate):
        if len(other_gate.inputs) < (2 if other_gate.gate_type in ["AND", "OR"] else 1):
            other_gate.inputs.append(self)
            self.connections.append(other_gate)
            self.app.mark_for_update(other_gate)  # Mark for update instead of calling update_all_connections directly

class LogicCircuitApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Logic Circuit Simulator")
        self.canvas = tk.Canvas(root, width=500, height=400, bg="white")
        self.canvas.pack()
        self.gates = []
        self.selected_gate = None
        self.pending_updates = set()  # Set to track gates that need updates
        self.add_buttons()
    
    def add_buttons(self):
        frame = tk.Frame(self.root)
        frame.pack()
        tk.Button(frame, text="Add AND Gate", command=lambda: self.add_gate("AND")).pack(side=tk.LEFT)
        tk.Button(frame, text="Add OR Gate", command=lambda: self.add_gate("OR")).pack(side=tk.LEFT)
        tk.Button(frame, text="Add NOT Gate", command=lambda: self.add_gate("NOT")).pack(side=tk.LEFT)
        tk.Button(frame, text="Reset Circuit", command=self.reset_circuit).pack(side=tk.LEFT)
    
    def add_gate(self, gate_type):
        gate = LogicGate(self, self.canvas, 50, 100, gate_type)
        self.gates.append(gate)
    
    def reset_circuit(self):
        self.canvas.delete("all")
        self.gates.clear()
        self.selected_gate = None
        self.pending_updates.clear()
    
    def mark_for_update(self, gate):
        """Mark a gate for update and process updates iteratively to avoid recursion limit."""
        self.pending_updates.add(gate)
        self.process_updates()
    
    def process_updates(self):
        """Iteratively update all marked gates."""
        while self.pending_updates:
            gate = self.pending_updates.pop()
            gate.update_output()

    def update_all_connections(self):
        """Mark all gates for updates and process them iteratively."""
        for gate in self.gates:
            self.mark_for_update(gate)

if __name__ == "__main__":
    root = tk.Tk()
    app = LogicCircuitApp(root)
    root.mainloop()
