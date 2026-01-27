import subprocess
import sys
import tkinter as tk
from functools import partial
from tkinter import ttk


class GravityTaskWindow(tk.Tk):
    def __init__(self, task, ex1, ex2, login):
        super().__init__()

        self.title("Закон всемирного тяготения")
        self.geometry(f'{800}x{600}')

        self.main_frame = tk.Frame(self)
        self.main_frame.grid(row=0, column=0, sticky="nsew")

        self.main_frame_2 = tk.Frame(self)
        self.main_frame_2.grid(row=1, column=0, sticky="nsew")

        self.right_frame = tk.Frame(self.main_frame)
        self.right_frame.grid(row=0, column=0, sticky="ns")

        self.left_frame = tk.Frame(self.main_frame)
        self.left_frame.grid(row=0, column=2, sticky="ns")

        self.separator = ttk.Separator(self.main_frame, orient="vertical")
        self.separator.grid(row=0, column=1, sticky="ns", padx=5)

        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=0)
        self.main_frame.grid_columnconfigure(2, weight=1)

        self.main_frame_2.grid_columnconfigure(0, weight=1)

        self.velocity = tk.DoubleVar()
        self.velocity.set(task.velocity if self.velocity is not None else 20000.0)

        #left
        tk.Label(
            self.right_frame,
            text="Задача:",
            font=("Tahoma", 16, "bold"),
        ).grid(row=0, column=0, sticky="nw", pady=10, padx=10)

        tk.Label(
            self.right_frame,
            text=task.text,
            font=("Tahoma", 13),
            wraplength=360
        ).grid(row=1, column=0, sticky="nw", pady=10, padx=10, rowspan = 3)

        tk.Label(
            self.right_frame,
            text="Результат:",
            font=("Tahoma", 16, "bold")
        ).grid(row=5, column=0, sticky="nw", pady=10, padx=10)

        tk.Label(
            self.right_frame,
            text='Попадание в мишень\nУпражнение 1: ' + ex1,
            font=("Tahoma", 13)
        ).grid(row=6, column=0, sticky= "nw")

        tk.Label(
            self.right_frame,
            text='Попадание в центр\nУпражнение 2: ' +  ex2,
            font=("Tahoma", 13)
        ).grid(row=7, column=0, sticky= "nw")


        #right
        tk.Label(
            self.left_frame,
            text="Скорость:",
            font=("Tahoma", 13),
            bg="#f0f0f0"
        ).grid(row=0, column=0, sticky="w", pady=10, padx=10)

        self.velocity = tk.Entry(
            self.left_frame,
            textvariable = self.velocity,
            font=("Tahoma", 13),
            width=25
        )
        self.velocity.grid(row=0, column=1, pady=10, padx=10)


        #start button
        login_button = tk.Button(
            self.main_frame_2,
            text="Запустить симуляцию",
            font=("Tahoma", 12, "bold"),
            bg="#3498db",
            fg="white",
            width=30,
            height=2,
            justify="center",
            command=partial(click, task),
            cursor="hand2"
        )
        login_button.grid(row = 0, column = 1, pady=100, padx=10, sticky = "s")

def click(task):
    if task.number == 4:
        subprocess.Popen([sys.executable, "Gravity.py"])