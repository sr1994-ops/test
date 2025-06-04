import tkinter as tk
import pyperclip

class ClipboardView(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Historial del Portapapeles")
        self.listbox = tk.Listbox(self, width=60, height=20)
        self.listbox.pack(fill=tk.BOTH, expand=True)
        self.listbox.bind('<Double-Button-1>', self.on_select)

    def update_list(self, history):
        self.listbox.delete(0, tk.END)
        for item in history:
            self.listbox.insert(tk.END, item)

    def on_select(self, event):
        selection = self.listbox.curselection()
        if selection:
            selected_text = self.listbox.get(selection[0])
            pyperclip.copy(selected_text)
            print(f"[Seleccionado] Copiado al portapapeles: {selected_text}")
            self.destroy()
