import tkinter as tk
from functools import partial

from ball_app import BallApp

class Task:
    def __init__(self, name, text, velocity, angle, x0, y0, Vmax, meter):
        super().__init__()

        self.name = name
        self.text = text
        self.velocity = velocity
        self.angle = angle
        self.x0 = x0
        self.y0 = y0
        self.Vmax = Vmax
        self.meter = meter

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Tasks")
        self.geometry(f'{800}x{600}')

        # self.tasks = ["Задание 1: Бросок мяча", "Задание 2: Бросок мяча", "Задание 3: Бросок мяча"]
        self.tasks= [
            Task(
                name="Задание 1: Бросок мяча",
                text="Текст номер 1",
                velocity=None,
                angle=45,
                x0 = 0,
                y0 = 0,
                Vmax=30,
                meter=10
            ),
            Task(
                name="Задание 2: Бросок мяча",
                text="Текст номер 2",
                velocity=50,
                angle=None,
                x0=0,
                y0=10,
                Vmax=200,
                meter=2
            ),
            Task(
                name="Задание 3: Бросок мяча",
                text="Текст номер 3",
                velocity=25,
                angle=33,
                x0=30,
                y0=50,
                Vmax=30,
                meter=5
            ),
        ]

        for task in self.tasks:
            self.task_name = tk.Label(text=task.name)
            self.task_name.grid(row=self.tasks.index(task), column=0, sticky=tk.NW)

            self.open_button = tk.Button(text="Open", command=partial(self.click, task))
            self.open_button.grid(row=self.tasks.index(task), column=1, sticky=tk.NW)


    def click(self, task):
        wind = BallApp(task)
        wind.grab_set()


if __name__ == '__main__':
    app = MainApp()
    app.mainloop()
    exit(0)