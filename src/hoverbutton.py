
import tkinter as tk

class HoverButton(tk.Button):
    def __init__(self, master, **kw):
        tk.Button.__init__(self, master=master, **kw)
        self.defaultBackground = self["background"]
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
        color = self["background"]
        rgb = tuple(int(color[i:i+2], 16) for i in (1, 3, 5))
        darker = tuple(max(0, c - 30) for c in rgb)
        self["background"] = f"#{darker[0]:02x}{darker[1]:02x}{darker[2]:02x}"

    def on_leave(self, e):
        self["background"] = self.defaultBackground
