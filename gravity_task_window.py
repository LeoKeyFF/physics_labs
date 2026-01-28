import math
import random
import subprocess
import sys
import tkinter as tk
from functools import partial
from tkinter import ttk, messagebox
import json

import database


G = 6.67430e-11  # Vonyuchaya constanta


class GravityTaskWindow(tk.Tk):
    def __init__(self, task, ex1, ex2, login):
        super().__init__()
        self.task = task
        self.task.radius = random.uniform(1.1, 4.4)
        self.task.radius = round(self.task.radius, 3) * 1e12

        self.task.velocity =  round(random.uniform(4000, 8000), 0)
        self.task.mass_big = (self.task.velocity ** 2 * self.task.radius) / G

        self.title("Закон всемирного тяготения")
        self.geometry(f'{800}x{600}')
        self.resizable(False, False)

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

        self.period = tk.DoubleVar()

        #left
        tk.Label(
            self.right_frame,
            text="Задача:",
            font=("Tahoma", 16, "bold"),
        ).grid(row=0, column=0, sticky="nw", pady=10, padx=10)

        tk.Label(
            self.right_frame,
            text=self.task.text1 + str(self.task.mass_big) + self.task.text2 + str(self.task.radius) + self.task.text3,
            font=("Tahoma", 13),
            wraplength=360
        ).grid(row=1, column=0, sticky="nw", pady=10, padx=10, rowspan = 3)

        # tk.Label(
        #     self.right_frame,
        #     text="Результат:",
        #     font=("Tahoma", 16, "bold")
        # ).grid(row=5, column=0, sticky="nw", pady=10, padx=10)
        #
        # tk.Label(
        #     self.right_frame,
        #     text='Погрешность не больше 5%\nУпражнение 1: ' + ex1,
        #     font=("Tahoma", 13)
        # ).grid(row=6, column=0, sticky= "nw")
        #
        # tk.Label(
        #     self.right_frame,
        #     text='Погрешность не больше 0,5%\nУпражнение 2: ' +  ex2,
        #     font=("Tahoma", 13)
        # ).grid(row=7, column=0, sticky= "nw")


        #right
        tk.Label(
            self.left_frame,
            text="Период:",
            font=("Tahoma", 13),
            bg="#f0f0f0"
        ).grid(row=0, column=0, sticky="w", pady=10, padx=10)

        self.period = tk.Entry(
            self.left_frame,
            textvariable = self.period,
            font=("Tahoma", 13),
            width=25
        )
        self.period.grid(row=0, column=1, pady=10, padx=10)


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
            command=partial(self.current_entry_value, ex1, ex2, login),
            cursor="hand2"
        )
        login_button.grid(row = 0, column = 1, pady=100, padx=10, sticky = "s")

    def current_entry_value(self, ex1, ex2, login):
        cur_val = self.period.get()
        if len(cur_val) == 0:
            messagebox.showerror("Ошибка", "Заполните значение!")
            return
        if float(cur_val) < 3e7:
            messagebox.showerror("Ошибка", "Слишком маленькое значение")
            return
        click(self.task, cur_val, ex1, ex2, login)


def click(task, period, ex1, ex2, login):
    # ----- json file: ------------------------------------
    data_to_save = {
        "period": period,
        "mass_big": task.mass_big,
        "radius": task.radius,
        "velocity": task.velocity
    }
    filename = 'data_to_gravity_sim.json'
    with open(filename, 'w') as file:
        json.dump(data_to_save, file, indent=4)

    # ---------------------------------------------------
    if task.number == 4:
        subprocess.Popen([sys.executable, "gravity_task_1.py"])

    t = 2 * math.pi * math.sqrt(task.radius ** 3 / (G * task.mass_big))
    if abs(t- float(period)) < t*0.01:
        if ex1 == "Не приступал(а)":
            database.add_result(task=task.number, exercise1=True, exercise2=True, login=login)

    elif abs(t- float(period)) < t*0.05:
        database.add_result(task=task.number, exercise1=True, exercise2=False, login=login)

    else:
        if ex1 == "Не приступал(а)":
            database.add_result(task=task.number, exercise1=False, exercise2=False, login=login)
