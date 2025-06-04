import threading
import keyboard
import queue
import json
import os

from models.clipboard_model import ClipboardModel
from views.clipboard_view import ClipboardView

class ClipboardController:
    def __init__(self, hotkey='ctrl+shift+h', config_file='config.json'):
        self.model = ClipboardModel()
        self.view = None
        self.command_queue = queue.Queue()
        self.config_file = config_file
        self.hotkey = hotkey
        self.load_config()
        self.setup_threads()

    def load_config(self):
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                config = json.load(f)
                self.hotkey = config.get('hotkey', self.hotkey)

    def save_config(self):
        with open(self.config_file, 'w') as f:
            json.dump({'hotkey': self.hotkey}, f)

    def start(self):
        print(f"Historial activo. Pulsa {self.hotkey} para abrir la ventana.")
        print("Puedes cambiar la combinación escribiendo 'hotkey <nueva combinación>' (ej: hotkey ctrl+alt+c). Escribe 'salir' para cerrar.")
        while True:
            cmd = input("Comando > ").strip().lower()
            self.command_queue.put(cmd)
            if cmd == "salir":
                break

    def setup_threads(self):
        threading.Thread(target=self.model.monitor_clipboard, args=(self.on_new_clipboard,), daemon=True).start()
        threading.Thread(target=self.command_listener, daemon=True).start()
        threading.Thread(target=self.hotkey_listener, daemon=True).start()

    def on_new_clipboard(self, text):
        print(f"[Nuevo] Copiado: {text}")

    def command_listener(self):
        while True:
            cmd = self.command_queue.get()
            if cmd == "ventana":
                self.show_window()
            elif cmd.startswith("hotkey "):
                new_hotkey = cmd.replace("hotkey ", "").strip()
                self.hotkey = new_hotkey
                self.save_config()
                keyboard.unhook_all_hotkeys()
                keyboard.add_hotkey(self.hotkey, lambda: self.command_queue.put("ventana"))
                print(f"[Configurado] Nueva combinación de teclas: {self.hotkey}")
            elif cmd == "salir":
                print("Saliendo...")
                break
            else:
                print("Comando no reconocido. Usa 'ventana', 'hotkey <combinación>' o 'salir'.")

    def hotkey_listener(self):
        keyboard.add_hotkey(self.hotkey, lambda: self.command_queue.put("ventana"))
        keyboard.wait()

    def show_window(self):
        self.view = ClipboardView()
        self.view.update_list(self.model.history)
        self.view.mainloop()
