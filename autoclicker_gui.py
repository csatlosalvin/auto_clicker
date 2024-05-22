import ctypes
import time
import threading
import tkinter as tk
from tkinter import messagebox

class AutoClicker:
    def __init__(self, root):
        self.root = root
        self.root.title("AutoClicker")
        self.root.geometry("300x200")
        self.root.protocol("WM_DELETE_WINDOW", self.hide_window)  # Az ablak bezárásának kezelése
        self.create_widgets()

    def create_widgets(self):
        self.label = tk.Label(self.root, text="Click interval (seconds):")
        self.label.pack(pady=10)
        
        self.interval_entry = tk.Entry(self.root)
        self.interval_entry.pack(pady=5)
        self.interval_entry.insert(0, "0.01")

        self.start_button = tk.Button(self.root, text="Start", command=self.start_autoclicker)
        self.start_button.pack(pady=5)

        self.stop_button = tk.Button(self.root, text="Stop", command=self.stop_autoclicker)
        self.stop_button.pack(pady=5)

    def click(self):
        ctypes.windll.user32.mouse_event(2, 0, 0, 0, 0)  # Bal gomb lenyomása
        ctypes.windll.user32.mouse_event(4, 0, 0, 0, 0)  # Bal gomb felengedése

    def autoclicker(self):
        while self.autoclicker_running:
            self.click()
            time.sleep(self.click_interval)

    def start_autoclicker(self):
        try:
            self.click_interval = float(self.interval_entry.get())
            if not self.autoclicker_running:
                self.autoclicker_running = True
                threading.Thread(target=self.autoclicker).start()
                messagebox.showinfo("Info", "AutoClicker started.")
            else:
                messagebox.showwarning("Warning", "AutoClicker is already running.")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number for the click interval.")

    def stop_autoclicker(self):
        self.autoclicker_running = False
        messagebox.showinfo("Info", "AutoClicker stopped.")

    def hide_window(self):
        # Az ablak elrejtése a bezárás helyett
        self.root.withdraw()

if __name__ == "__main__":
    root = tk.Tk()
    app = AutoClicker(root)
    root.deiconify()  # Az ablak megjelenítése
    root.mainloop()
