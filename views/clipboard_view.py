import tkinter as tk
from tkinter import ttk
import pyperclip

class ClipboardView(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Historial del Portapapeles")
        self.configure(bg="white")
        self.resizable(False, False)
        self.attributes("-topmost", True)

        # Coloca la ventana cerca del puntero del ratón
        self.update_idletasks()
        x, y = self.winfo_pointerxy()
        self.geometry(f"+{x+10}+{y+10}")

        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        self.listbox = tk.Listbox(self, width=60, height=20, bd=0, highlightthickness=0)
        self.listbox.pack(fill=tk.BOTH, expand=True)
        self.listbox.bind("<Double-Button-1>", self.on_select)

        # Cerrar al perder el foco o al hacer clic fuera
        self.bind("<FocusOut>", lambda e: self.destroy())

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
