import pyperclip
import time

class ClipboardModel:
    def __init__(self, max_history=20):
        self.history = []
        self.max_history = max_history
        self.last_text = ""

    def monitor_clipboard(self, callback=None):
        while True:
            try:
                current_text = pyperclip.paste()
                if current_text != self.last_text:
                    if current_text.strip() != "":
                        self.history.append(current_text)
                        if len(self.history) > self.max_history:
                            self.history.pop(0)
                        if callback:
                            callback(current_text)
                    self.last_text = current_text
            except Exception as e:
                print(f"Error: {e}")
            time.sleep(0.5)
