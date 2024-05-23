import ctypes
import time
import threading
import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog

class AutoClicker:
    def __init__(self, root):
        self.root = root
        self.root.title("AutoClicker")
        self.root.geometry("300x250")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)  # Ablak bezárásának kezelése

        self.autoclicker_running = False
        self.click_interval = 0.1  # Alapértelmezett kattintási időköz
        self.click_mode = "Continuous"  # Alapértelmezett kattintási mód

        self.create_widgets()

    def create_widgets(self):
        self.label_interval = tk.Label(self.root, text="Kattintási időköz (másodpercekben):")
        self.label_interval.pack(pady=5)

        self.interval_entry = tk.Entry(self.root)
        self.interval_entry.pack(pady=5)
        self.interval_entry.insert(0, str(self.click_interval))

        self.label_mode = tk.Label(self.root, text="Kattintási mód:")
        self.label_mode.pack(pady=5)

        self.mode_var = tk.StringVar()
        self.mode_var.set("Continuous")

        self.mode_menu = tk.OptionMenu(self.root, self.mode_var, "Continuous", "Single", "Cyclic")
        self.mode_menu.pack(pady=5)

        self.start_button = tk.Button(self.root, text="Start", command=self.start_autoclicker)
        self.start_button.pack(pady=5)

        self.stop_button = tk.Button(self.root, text="Stop", command=self.stop_autoclicker)
        self.stop_button.pack(pady=5)

        self.settings_button = tk.Button(self.root, text="Settings", command=self.open_settings)
        self.settings_button.pack(pady=5)

    def click(self):
        ctypes.windll.user32.mouse_event(2, 0, 0, 0, 0)  # Bal gomb lenyomása
        ctypes.windll.user32.mouse_event(4, 0, 0, 0, 0)  # Bal gomb felengedése

    def autoclicker(self):
        while self.autoclicker_running:
            if self.click_mode == "Single":
                self.click()
                self.stop_autoclicker()
            elif self.click_mode == "Continuous":
                self.click()
            elif self.click_mode == "Cyclic":
                self.click()
                time.sleep(self.click_interval)
            time.sleep(self.click_interval)

    def start_autoclicker(self):
        try:
            self.click_interval = float(self.interval_entry.get())
            self.click_mode = self.mode_var.get()
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

    def open_settings(self):
        new_interval = simpledialog.askfloat("Settings", "Enter new click interval (seconds):", initialvalue=self.click_interval)
        if new_interval is not None:
            self.click_interval = new_interval
            messagebox.showinfo("Info", "Settings saved.")

    def on_closing(self):
        if self.autoclicker_running:
            self.autoclicker_running = False
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = AutoClicker(root)
    root.mainloop()
