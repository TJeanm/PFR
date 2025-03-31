import tkinter as tk

# Commandes pour la voiture
COMMANDS = {
    "forward": "F",
    "backward": "B",
    "left": "L",
    "right": "R",
    "stop": "S"
}

# Interface graphique Tkinter
class RemoteControlApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Télécommande")
        self.root.geometry("300x300")
        
        self.create_buttons()
        self.root.bind_all("<KeyPress>", self.key_pressed)
        self.root.bind_all("<KeyRelease>", self.key_released)
    
    def create_buttons(self):
        self.btn_forward = tk.Button(self.root, text="↑", width=10, height=2, command=lambda: self.send_command("forward"))
        self.btn_forward.grid(row=0, column=1)
        
        self.btn_left = tk.Button(self.root, text="←", width=10, height=2, command=lambda: self.send_command("left"))
        self.btn_left.grid(row=1, column=0)
        
        self.btn_stop = tk.Button(self.root, text="⏹️ STOP", width=10, height=2, command=lambda: self.send_command("stop"))
        self.btn_stop.grid(row=1, column=1)
        
        self.btn_right = tk.Button(self.root, text="→", width=10, height=2, command=lambda: self.send_command("right"))
        self.btn_right.grid(row=1, column=2)
        
        self.btn_backward = tk.Button(self.root, text="↓", width=10, height=2, command=lambda: self.send_command("backward"))
        self.btn_backward.grid(row=2, column=1)
    
    def send_command(self, action):
        print(f"📤 Commande envoyée : {COMMANDS[action]}")
    
    def key_pressed(self, event):
        key_map = {"w": "forward", "s": "backward", "a": "left", "d": "right"}
        if event.keysym in key_map:
            self.send_command(key_map[event.keysym])
    
    def key_released(self, event):
        self.send_command("stop")

if __name__ == "__main__":
    root = tk.Tk()
    app = RemoteControlApp(root)
    root.mainloop()
