import pyperclip
import time
import threading
import tkinter as tk
import queue
import keyboard  # asegúrate de instalarlo con 'pip install keyboard'
import json
import os

clipboard_history = []
max_history = 20
command_queue = queue.Queue()
config_file = 'config.json'

# Cargar configuración previa si existe
if os.path.exists(config_file):
    with open(config_file, 'r') as f:
        config = json.load(f)
        HOTKEY_COMBINATION = config.get('hotkey', 'ctrl+shift+h')
else:
    HOTKEY_COMBINATION = 'ctrl+shift+h'

def save_config():
    with open(config_file, 'w') as f:
        json.dump({'hotkey': HOTKEY_COMBINATION}, f)

def monitor_clipboard():
    last_text = ""
    while True:
        try:
            current_text = pyperclip.paste()
            if current_text != last_text:
                if current_text.strip() != "":
                    clipboard_history.append(current_text)
                    if len(clipboard_history) > max_history:
                        clipboard_history.pop(0)
                    print(f"[Nuevo] Copiado: {current_text}")
                last_text = current_text
        except Exception as e:
            print(f"Error: {e}")
        time.sleep(0.5)

def show_history_window():
    root = tk.Tk()
    root.title("Historial del Portapapeles")

    listbox = tk.Listbox(root, width=60, height=20)
    listbox.pack(fill=tk.BOTH, expand=True)

    for item in clipboard_history:
        listbox.insert(tk.END, item)

    def on_select(event):
        selection = listbox.curselection()
        if selection:
            selected_text = listbox.get(selection[0])
            pyperclip.copy(selected_text)
            print(f"[Seleccionado] Copiado al portapapeles: {selected_text}")
            root.destroy()

    listbox.bind('<Double-Button-1>', on_select)
    root.mainloop()

def command_listener():
    global HOTKEY_COMBINATION
    while True:
        cmd = command_queue.get()
        if cmd == "ventana":
            show_history_window()
        elif cmd.startswith("hotkey "):
            new_hotkey = cmd.replace("hotkey ", "").strip()
            HOTKEY_COMBINATION = new_hotkey
            save_config()
            keyboard.unhook_all_hotkeys()
            keyboard.add_hotkey(HOTKEY_COMBINATION, lambda: command_queue.put("ventana"))
            print(f"[Configurado] Nueva combinación de teclas: {HOTKEY_COMBINATION}")
        elif cmd == "salir":
            print("Saliendo...")
            break
        else:
            print("Comando no reconocido. Usa 'ventana', 'hotkey <combinación>' o 'salir'.")

def hotkey_listener():
    keyboard.add_hotkey(HOTKEY_COMBINATION, lambda: command_queue.put("ventana"))
    keyboard.wait()

if __name__ == "__main__":
    threading.Thread(target=monitor_clipboard, daemon=True).start()
    threading.Thread(target=command_listener, daemon=True).start()
    threading.Thread(target=hotkey_listener, daemon=True).start()

    print(f"Historial activo. Pulsa {HOTKEY_COMBINATION} para abrir la ventana.")
    print("Puedes cambiar la combinación escribiendo 'hotkey <nueva combinación>' (ej: hotkey ctrl+alt+c). Escribe 'salir' para cerrar.")

    while True:
        cmd = input("Comando > ").strip().lower()
        command_queue.put(cmd)
        if cmd == "salir":
            break
