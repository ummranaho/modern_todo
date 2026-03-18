import tkinter as tk
from tkinter import messagebox
import json
import os
import glob
import sys

# ==============================
# Configuration
# ==============================
APP_NAME = "Modern To-Do"
FILE_NAME = "tasks.json"

BG_COLOR = "#0f172a"
CARD_COLOR = "#1e293b"
ACCENT = "#3b82f6"
SUCCESS = "#22c55e"
DANGER = "#ef4444"
TEXT_COLOR = "#f8fafc"
MUTED = "#94a3b8"

FONT_TITLE = ("Segoe UI", 22, "bold")
FONT_NORMAL = ("Segoe UI", 12)
FONT_SMALL = ("Segoe UI", 10)

# ==============================
# Main App Class
# ==============================
class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title(APP_NAME)
        self.root.geometry("520x650")
        self.root.config(bg=BG_COLOR)
        self.root.resizable(False, False)

        # Set window icon (generated)
        self.set_icon()

        self.tasks = []
        self.load_tasks()

        self.create_ui()
        self.render_tasks()

    # ==============================
    # UI Setup
    # ==============================
    def create_ui(self):
        # Title
        title = tk.Label(
            self.root,
            text="📝 My Tasks",
            bg=BG_COLOR,
            fg=TEXT_COLOR,
            font=FONT_TITLE
        )
        title.pack(pady=20)

        # Input Frame
        input_frame = tk.Frame(self.root, bg=BG_COLOR)
        input_frame.pack(pady=10)

        self.task_entry = tk.Entry(
            input_frame,
            width=30,
            font=FONT_NORMAL,
            bg=CARD_COLOR,
            fg=TEXT_COLOR,
            insertbackground=TEXT_COLOR,
            relief="flat"
        )
        self.task_entry.pack(side="left", ipady=8, padx=(0, 10))

        add_btn = tk.Button(
            input_frame,
            text="Add",
            bg=ACCENT,
            fg="white",
            font=FONT_NORMAL,
            relief="flat",
            command=self.add_task
        )
        add_btn.pack(side="left", ipadx=10, ipady=5)

        # Task Container
        self.task_frame = tk.Frame(self.root, bg=BG_COLOR)
        self.task_frame.pack(pady=20, fill="both", expand=True)

        # Footer
        footer = tk.Label(
            self.root,
            text="Built with Python & Tkinter",
            bg=BG_COLOR,
            fg=MUTED,
            font=FONT_SMALL
        )
        footer.pack(pady=10)

    # ==============================
    # Task Logic
    # ==============================
    def add_task(self):
        task_text = self.task_entry.get().strip()
        if task_text == "":
            messagebox.showwarning("Warning", "Task cannot be empty!")
            return

        self.tasks.append({"text": task_text, "done": False})
        self.task_entry.delete(0, tk.END)
        self.save_tasks()
        self.render_tasks()

    def delete_task(self, index):
        del self.tasks[index]
        self.save_tasks()
        self.render_tasks()

    def toggle_task(self, index):
        self.tasks[index]["done"] = not self.tasks[index]["done"]
        self.save_tasks()
        self.render_tasks()

    # ==============================
    # Render Tasks
    # ==============================
    def render_tasks(self):
        for widget in self.task_frame.winfo_children():
            widget.destroy()

        for index, task in enumerate(self.tasks):
            card = tk.Frame(self.task_frame, bg=CARD_COLOR)
            card.pack(fill="x", pady=5, padx=20)

            task_text = task["text"]
            done = task["done"]

            label = tk.Label(
                card,
                text=task_text,
                bg=CARD_COLOR,
                fg=SUCCESS if done else TEXT_COLOR,
                font=FONT_NORMAL,
                anchor="w"
            )
            label.pack(side="left", padx=10, pady=10, fill="x", expand=True)

            if done:
                label.config(text="✔ " + task_text)

            label.bind("<Button-1>", lambda e, i=index: self.toggle_task(i))

            del_btn = tk.Button(
                card,
                text="✖",
                bg=DANGER,
                fg="white",
                relief="flat",
                command=lambda i=index: self.delete_task(i)
            )
            del_btn.pack(side="right", padx=10, pady=5)

    # ==============================
    # File Storage
    # ==============================
    def save_tasks(self):
        with open(FILE_NAME, "w") as f:
            json.dump(self.tasks, f)

    def load_tasks(self):
        if os.path.exists(FILE_NAME):
            with open(FILE_NAME, "r") as f:
                self.tasks = json.load(f)

    # ==============================
    # Icon Creation
    # ==============================
    def set_icon(self):
        # Try loading an icon file from assets/icon/ (prefer .ico on Windows),
        # otherwise fall back to a generated image.
        
        # Handle PyInstaller compiled mode
        if getattr(sys, 'frozen', False):
            base_dir = sys._MEIPASS
        else:
            base_dir = os.path.dirname(__file__)
        
        icon_dir = os.path.join(base_dir, "assets", "icon")

        if os.path.isdir(icon_dir):
            # Prefer .ico, then common image formats
            for pattern in ("*.ico", "*.png", "*.gif"):
                matches = glob.glob(os.path.join(icon_dir, pattern))
                if matches:
                    path = matches[0]
                    try:
                        if path.lower().endswith('.ico'):
                            # iconbitmap works well for .ico on Windows
                            self.root.iconbitmap(path)
                        else:
                            img = tk.PhotoImage(file=path)
                            self.root.iconphoto(False, img)
                            # keep reference to avoid garbage collection
                            self._icon_image = img
                        return
                    except Exception:
                        # If loading fails, continue to fallback
                        pass

        # Fallback: generated icon
        icon = tk.PhotoImage(width=64, height=64)
        icon.put(ACCENT, to=(0, 0, 64, 64))
        icon.put("white", to=(20, 20, 44, 44))
        self.root.iconphoto(False, icon)
        self._icon_image = icon

# ==============================
# Run App
# ==============================
if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()
