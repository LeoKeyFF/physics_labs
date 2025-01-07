import tkinter as tk
from ball_app import BallApp


class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Tasks")
        self.geometry(f'{800}x{600}')

        self.tasks = ["Задание 1: Бросок мяча", "Задание 2: Бросок мяча", "Задание 3: Бросок мяча"]

        for task in self.tasks:
            self.task_name = tk.Label(text=task)
            self.task_name.grid(row=self.tasks.index(task), column=0, sticky=tk.NW)

            self.open_button = tk.Button(text="Open", command=self.click)
            self.open_button.grid(row=self.tasks.index(task), column=1, sticky=tk.NW)


    def click(self):
        wind = BallApp()
        wind.grab_set()


if __name__ == '__main__':
    app = MainApp()
    app.mainloop()
    exit(0)