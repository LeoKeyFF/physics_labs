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
        if self.task.number == 4:
            self.task.radius = random.uniform(1.1, 4.4)
            self.task.radius = round(self.task.radius, 3) * 1e12
            self.task.velocity =  round(random.uniform(4000, 8000), 0)
            self.task.mass_big = (self.task.velocity ** 2 * self.task.radius) / G
        else:
            self.task.period = random.uniform(2.8 * math. pi, 22.0 * math. pi)
            self.task.period = round(self.task.period, 3) * 1e8
            self.task.radius = random.uniform(1.1, 4.4)
            self.task.radius = round(self.task.radius, 3) * 1e12
            self.task.velocity = 2 * math. pi * self.task.radius / self.task.period

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

        self.period_var = tk.DoubleVar()
        self.mass_big_var = tk.DoubleVar()

        self.ex1 = ex1
        self.ex2 = ex2

        #left
        tk.Label(
            self.right_frame,
            text="Задача:",
            font=("Tahoma", 16, "bold"),
        ).grid(row=0, column=0, sticky="nw", pady=10, padx=10)

        if self.task.number == 4:
            tk.Label(
                self.right_frame,
                text=self.task.text1 + str(self.task.mass_big) + self.task.text2 + str(self.task.radius) + self.task.text3,
                font=("Tahoma", 13),
                wraplength=360
            ).grid(row=1, column=0, sticky="nw", pady=10, padx=10, rowspan = 3)
        else:
            tk.Label(
                self.right_frame,
                text=self.task.text1 + str(self.task.radius) + self.task.text2 + str(self.task.period) + self.task.text3,
                font=("Tahoma", 13),
                wraplength=360
            ).grid(row=1, column=0, sticky="nw", pady=10, padx=10, rowspan = 3)

        self.res_frame = tk.Frame(self.right_frame)
        self.res_frame.grid(row=5, column=0, sticky="ns")

        self.draw_result()

        #right
        if self.task.number == 4:
            tk.Label(
                self.left_frame,
                text="Период:",
                font=("Tahoma", 13),
                bg="#f0f0f0"
            ).grid(row=0, column=0, sticky="w", pady=10, padx=10)

            self.period_var = tk.Entry(
                self.left_frame,
                textvariable = self.period_var,
                font=("Tahoma", 13),
                width=25
            )
            self.period_var.grid(row=0, column=1, pady=10, padx=10)
        else:
            tk.Label(
                self.left_frame,
                text="Масса:",
                font=("Tahoma", 13),
                bg="#f0f0f0"
            ).grid(row=0, column=0, sticky="w", pady=10, padx=10)

            self.mass_big_var = tk.Entry(
                self.left_frame,
                textvariable=self.mass_big_var,
                font=("Tahoma", 13),
                width=25
            )
            self.mass_big_var.grid(row=0, column=1, pady=10, padx=10)


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

    def draw_result(self):
        for widget in self.res_frame.winfo_children():
            widget.destroy()
        tk.Label(
            self.res_frame,
            text="Результат:",
            font=("Tahoma", 16, "bold")
        ).grid(row=0, column=0, sticky="nw", pady=10, padx=10)

        tk.Label(
            self.res_frame,
            text='Погрешность не больше 5%\nУпражнение 1: ' + self.ex1,
            font=("Tahoma", 13)
        ).grid(row=1, column=0, sticky= "nw")

        tk.Label(
            self.res_frame,
            text='Погрешность не больше 1%\nУпражнение 2: ' +  self.ex2,
            font=("Tahoma", 13)
        ).grid(row=2, column=0, sticky= "nw")

    def current_entry_value(self, ex1, ex2, login):
        if self.task.number == 4:
            cur_val = self.period_var.get()
        else:
            cur_val = self.mass_big_var.get()
        if len(cur_val) == 0:
            messagebox.showerror("Ошибка", "Заполните значение!")
            return
        if float(cur_val) < 3e7:
            messagebox.showerror("Ошибка", "Слишком маленькое значение")
            return

        # Проверка------------------------4
        if self.task.number == 4:
            right = 2 * math.pi * math.sqrt(self.task.radius ** 3 / (G * self.task.mass_big))
        else:
            right = 4*math.pi**2*self.task.radius**3/(G*self.task.period**2)

        if abs(right - float(cur_val)) < right * 0.01:
            database.add_result(task=self.task.number, exercise1=True, exercise2=True, login=login)
            self.ex1 = "Правильно"
            self.ex2 = "Правильно"
            self.draw_result()

        elif abs(right - float(cur_val)) < right * 0.05:
            database.add_result(task=self.task.number, exercise1=True, exercise2=False, login=login)
            self.ex1 = "Правильно"
            self.ex2 = "Ошибка"
            self.draw_result()

        else:
            if self.ex1 == "Не приступал(а)":
                database.add_result(task=self.task.number, exercise1=False, exercise2=False, login=login)
                self.ex1 = "Ошибка"
                self.ex2 = "Ошибка"
                self.draw_result()
        if self.task.number == 4:
            click(self.task, self.task.mass_big, cur_val)
        else:
            click(self.task, cur_val, self.task.period)



def click(task, mass, period):
    # ----- json file: ------------------------------------
    data_to_save = {
        "period": period,
        "mass_big": mass,
        "radius": task.radius,
        "velocity": task.velocity
    }
    filename = 'data_to_gravity_sim.json'
    with open(filename, 'w') as file:
        json.dump(data_to_save, file, indent=4)

    # ---------------------------------------------------
    if task.number == 4:
        subprocess.Popen([sys.executable, "gravity_task_1.py"])
    elif task.number == 5:
        subprocess.Popen([sys.executable, "gravity_task_2.py"])


