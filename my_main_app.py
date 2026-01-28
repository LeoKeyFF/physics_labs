import tkinter as tk
from functools import partial
from tkinter import ttk, messagebox

import database
from ball_app import BallApp
from gravity_task_window import GravityTaskWindow
from scrollable_frame import ScrollableFrame
from task_class import TaskBall, TaskGravity



def click(task, task_number, login):
    stat = database.get_stat()
    stat_local = [item for item in stat if item.get("login") == login and item.get("task_number") == task_number]
    ex1 = stat_local[0]["ex1"]
    ex2 = stat_local[0]["ex2"]

    if task_number in [1,2,3]:
        wind = BallApp(task, ex1, ex2, login)
        wind.grab_set()
    else:
        wind = GravityTaskWindow(task, ex1, ex2, login)
        wind.grab_set()


def create_task_block(parent_frame, block_title, tasks, login):

    block_frame = tk.Frame(parent_frame, bg="#ecf0f1", relief="groove", bd=2)
    block_frame.pack(fill="x", padx=20, pady=10)

    title_frame = tk.Frame(block_frame, bg="#3498db")
    title_frame.pack(fill="x")

    tk.Label(
        title_frame,
        text=block_title,
        font=("Tahoma", 14, "bold"),
        bg="#3498db",
        fg="white",
        pady=10
    ).pack()

    tasks_frame = tk.Frame(block_frame, bg="#ecf0f1")
    tasks_frame.pack(fill="x", padx=10, pady=15)

    for task in tasks:
        task_frame = tk.Frame(tasks_frame, bg="white", relief="solid", bd=1)
        task_frame.pack(fill="x", padx=5, pady=5)

        (tk.Label(
            task_frame,
            text=task.name,
            font=("Tahoma", 12, "bold"),
            bg="white",
            fg="#2c3e50",
            width=65,
            justify="center"
        ).pack(anchor="w", padx=10, pady=(5, 0)))

        tk.Button(
            task_frame,
            text="Открыть задачу",
            font=("Tahoma", 10),
            bg="#3498db",
            fg="white",
            cursor="hand2",
            command=partial(click, task, task.number, login)
        ).pack(anchor="e", padx=10, pady=(0, 5))

    return block_frame


def create_stat_block(parent_frame, login, stat):
    table_frame = tk.Frame(parent_frame, bg="white", relief="solid", bd=1)
    table_frame.pack(fill="x", padx=20, pady=20)

    # Заголовок таблицы с именем исполнителя
    header_frame = tk.Frame(table_frame, bg="#2c3e50")
    header_frame.pack(fill="x")

    # Название таблицы с исполнителем
    tk.Label(
        header_frame,
        text=login,
        font=("Tahoma", 12, "bold"),
        bg="#2c3e50",
        fg="white",
        pady=10
    ).pack()

    # Заголовки столбцов таблицы
    columns_frame = tk.Frame(table_frame, bg="#3498db")
    columns_frame.pack(fill="x")

    headers = ["№ Задания", "Упражнение 1", "Упражнение 2"]

    for col, header in enumerate(headers):
        label = tk.Label(
            columns_frame,
            text=header,
            font=("Tahoma", 11, "bold"),
            bg="#3498db",
            fg="white",
            padx=10,
            pady=8,
            width=25,
            justify="center",
            wraplength=250
        )
        label.grid(row=0, column=col)
        label.config(anchor="center")

    columns_frame.grid_columnconfigure(0, weight=1)
    columns_frame.grid_columnconfigure(1, weight=1)
    columns_frame.grid_columnconfigure(2, weight=1)


    for row, statistic in enumerate(stat, start=1):

        row_color = "#f8f9fa" if row % 2 == 0 else "white"
        row_frame = tk.Frame(table_frame, bg=row_color)
        row_frame.pack(fill="x")

        label_id = tk.Label(
            row_frame,
            text=str(statistic["task_number"]),
            font=("Tahoma", 10, "bold"),
            bg=row_color,
            padx=0,
            pady=10,
            width=22,
            justify="center"
        )
        label_id.grid(row=0, column=0)
        label_id.config(anchor="center")

        label_ex1 = tk.Label(
            row_frame,
            text=str(statistic["ex1"]),
            font=("Tahoma", 10),
            bg=row_color,
            padx=0,
            pady=10,
            width=22,
            justify="center"
        )
        label_ex1.grid(row=0, column=1)
        label_ex1.config(anchor="center")

        label_ex2 = tk.Label(
            row_frame,
            text=str(statistic["ex2"]),
            font=("Tahoma", 10),
            bg=row_color,
            padx=0,
            pady=10,
            width=22,
            justify="center"
        )
        label_ex2.grid(row=0, column=2)
        label_ex2.config(anchor="center")

        row_frame.grid_columnconfigure(0, weight=1)
        row_frame.grid_columnconfigure(1, weight=1)
        row_frame.grid_columnconfigure(2, weight=1)


    return table_frame


class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Главная")
        self.geometry(f'{800}x{600}')
        self.resizable(False, False)

        self.main_frame = tk.Frame(self)
        self.main_frame.pack(fill="both", expand=True)

        self.current_user = None

        self.tasks_ball= [
            TaskBall(
                number = 1,
                name="Задание 1: Баскетболист и мяч",
                text="Баскетболист бросает мяч в щит кольца под углом 50 градусов (от горизонта). "
                     "С какой скоростью (м/с) нужно бросить мяч, чтобы попасть в центр щита и забить гол?",
                velocity=None,
                angle=50.0,
                x0 = 0,
                y0 = 0,
                Vmax=13.0,
                meter=50
            ),
            TaskBall(
                number=2,
                name="Задание 2: Пушка и снаряд",
                text="Пушка выпускает снаряд с начальной скоростью 300 м/с с холма высотой 2 км по мишени."
                     "При каком угле наклона орудия снаряд попадёт в цель?",
                velocity=300.0,
                angle=None,
                x0=0,
                y0=2000,
                Vmax=300,
                meter=0.1
            ),
            TaskBall(
                number=3,
                name="Задание 3: Скалолаз и карабин",
                text="Скалолаз на склоне должен метнуть карабин с верёвкой своему "
                     "напарнику. Карабин бросают рукой со скоростью 22 м/с. "
                     "Под каким углом к горизонту надо его бросить, чтобы он точно достиг цели? ",
                velocity=22.0,
                angle=None,
                x0=10,
                y0=20,
                Vmax=22.0,
                meter=10
            ),
        ]

        self.tasks_gravity= [
            TaskGravity(
                number = 4,
                name="Задание 4: Планета и спутник",
                text1="Вокруг планеты массой ",
                text2= " кг на орбите радиуса (считая от центра объекта) ",
                text3= " м крутится спутник, рассчитайте с каким периодом (с) будет совершаться полный оборот."
            )
        ]

        self.show_login_window()

    def show_login_window(self):
        self.clear_main_frame()

        title_label = tk.Label(
            self.main_frame,
            text="Вход в систему",
            font=("Tahoma", 24, "bold"),
            bg="#f0f0f0",
            fg="#333"
        )
        title_label.pack(pady=(50, 30))

        # Фрейм для формы
        form_frame = tk.Frame(self.main_frame)
        form_frame.pack(pady=20)

        # Поле для логина
        tk.Label(
            form_frame,
            text="Логин:",
            font=("Tahoma", 12),
            bg="#f0f0f0"
        ).grid(row=0, column=0, sticky="w", pady=10, padx=10)

        self.login_entry = tk.Entry(
            form_frame,
            font=("Tahoma", 12),
            width=25
        )
        self.login_entry.grid(row=0, column=1, pady=10, padx=10)

        # Поле для пароля
        tk.Label(
            form_frame,
            text="Пароль:",
            font=("Tahoma", 12),
            bg="#f0f0f0"
        ).grid(row=1, column=0, sticky="w", pady=10, padx=10)

        self.password_entry = tk.Entry(
            form_frame,
            font=("Tahoma", 12),
            width=25,
            show="*"
        )
        self.password_entry.grid(row=1, column=1, pady=10, padx=10)

        # Кнопка входа
        login_button = tk.Button(
            self.main_frame,
            text="Войти",
            font=("Tahoma", 12, "bold"),
            bg="#4CAF50",
            fg="white",
            width=15,
            height=2,
            command=self.sign_in,
            cursor="hand2"
        )
        login_button.pack(pady=30)

        # Ссылка на регистрацию
        switch_frame = tk.Frame(self.main_frame, bg="#f0f0f0")
        switch_frame.pack(pady=20)

        tk.Label(
            switch_frame,
            text="Нет аккаунта?",
            font=("Tahoma", 10),
            bg="#f0f0f0"
        ).pack(side="left", padx=(0, 5))

        register_link = tk.Label(
            switch_frame,
            text="Зарегистрироваться",
            font=("Tahoma", 10, "underline"),
            bg="#f0f0f0",
            fg="blue",
            cursor="hand2"
        )
        register_link.pack(side="left")
        register_link.bind("<Button-1>", lambda e: self.show_register_window())

    def show_register_window(self):

        self.clear_main_frame()

        # Заголовок
        title_label = tk.Label(
            self.main_frame,
            text="Регистрация",
            font=("Tahoma", 24, "bold"),
            bg="#f0f0f0",
            fg="#333"
        )
        title_label.pack(pady=(50, 30))

        # Фрейм для формы
        form_frame = tk.Frame(self.main_frame)
        form_frame.pack(pady=20)

        # Поле для логина
        tk.Label(
            form_frame,
            text="Логин:",
            font=("Tahoma", 12),
            bg="#f0f0f0"
        ).grid(row=0, column=0, sticky="w", pady=10, padx=10)

        self.reg_login_entry = tk.Entry(
            form_frame,
            font=("Tahoma", 12),
            width=25
        )
        self.reg_login_entry.grid(row=0, column=1, pady=10, padx=10)

        self.status_combo = ttk.Combobox(
            self.main_frame,
            values=["Ученик", "Учитель"],
            font=("Tahoma", 11),
            state="readonly",
            width=23
        )
        self.status_combo.pack(pady=(0, 10))
        self.status_combo.set("Ученик")

        # Поле для пароля
        tk.Label(
            form_frame,
            text="Пароль:",
            font=("Tahoma", 12),
            bg="#f0f0f0"
        ).grid(row=2, column=0, sticky="w", pady=10, padx=10)

        self.reg_password_entry = tk.Entry(
            form_frame,
            font=("Tahoma", 12),
            width=25,
            show="*"
        )
        self.reg_password_entry.grid(row=2, column=1, pady=10, padx=10)

        # Поле для подтверждения пароля
        tk.Label(
            form_frame,
            text="Подтвердите пароль:",
            font=("Tahoma", 12),
            bg="#f0f0f0"
        ).grid(row=3, column=0, sticky="w", pady=10, padx=10)

        self.confirm_password_entry = tk.Entry(
            form_frame,
            font=("Tahoma", 12),
            width=25,
            show="*"
        )
        self.confirm_password_entry.grid(row=3, column=1, pady=10, padx=10)

        # Кнопка регистрации
        register_button = tk.Button(
            self.main_frame,
            text="Зарегистрироваться",
            font=("Tahoma", 12, "bold"),
            bg="#2196F3",
            fg="white",
            width=20,
            height=2,
            command=self.sign_up,
            cursor="hand2"
        )
        register_button.pack(pady=30)

        # Ссылка на вход
        switch_frame = tk.Frame(self.main_frame, bg="#f0f0f0")
        switch_frame.pack(pady=20)

        tk.Label(
            switch_frame,
            text="Уже есть аккаунт?",
            font=("Tahoma", 10),
            bg="#f0f0f0"
        ).pack(side="left", padx=(0, 5))

        login_link = tk.Label(
            switch_frame,
            text="Войти",
            font=("Tahoma", 10, "underline"),
            bg="#f0f0f0",
            fg="blue",
            cursor="hand2"
        )
        login_link.pack(side="left")
        login_link.bind("<Button-1>", lambda e: self.show_login_window())

    def clear_main_frame(self):
        """Очистить основной фрейм"""
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def sign_up(self):
        login = self.reg_login_entry.get()
        password = self.reg_password_entry.get()
        confirm_password = self.confirm_password_entry.get()
        status_text = self.status_combo.get()
        if status_text == "Ученик":
            status = "student"
        else:
            status = "teacher"

        if not all([login, password, confirm_password]):
            messagebox.showwarning("Внимание", "Все поля должны быть заполнены!")
            return

        if password != confirm_password:
            messagebox.showwarning("Внимание", "Пароли не совпадают!")
            return

        if not database.acc_check_for_same_user_name(login):
            messagebox.showwarning("Внимание", "Имя пользователя уже занято")
            return

        database.acc_sign_up(login, password, status)

        messagebox.showinfo("Успех", "Регистрация прошла успешно!")

        self.show_login_window()

    def sign_in(self):
        login = self.login_entry.get()
        password = self.password_entry.get()

        if not all([login, password]):
            messagebox.showwarning("Внимание", "Заполните все поля!")
            return

        if database.sign_in(login, password) is None:
            messagebox.showerror("Ошибка", "Пользователь не найден")

        elif not database.sign_in(login, password):
            messagebox.showerror("Ошибка", "Неверный логин или пароль")

        else:
            self.current_user = login
            status = database.sign_in(login, password)
            if status == "student":
                self.show_student_window()
            else:
                self.show_teacher_window()
            messagebox.showinfo("Успех", "Вход выполнен успешно!")

    def show_student_window(self):
        self.clear_main_frame()

        self.create_user_header(self.main_frame, self.current_user)


        scroll_frame = ScrollableFrame(self.main_frame)
        scroll_frame.pack(fill="both", expand=True)

        # Заголовок экрана
        tk.Label(
            scroll_frame.scrollable_frame,
            text="📚 Задачи",
            font=("Tahoma", 20, "bold"),
            fg="#2c3e50"
        ).pack(pady=(20, 10))

        create_task_block(scroll_frame.scrollable_frame, "Баллистические задачи", self.tasks_ball, self.current_user)

        create_task_block(scroll_frame.scrollable_frame, "Закон всемирного тяготения", self.tasks_gravity, self.current_user)

    def show_teacher_window(self):
        self.clear_main_frame()

        self.create_user_header(self.main_frame, self.current_user)

        stat = database.get_stat()
        logins = list(set([item['login'] for item in stat]))

        scroll_frame = ScrollableFrame(self.main_frame)
        scroll_frame.pack(fill="both", expand=True)

        tk.Label(
            scroll_frame.scrollable_frame,
            text="Статистика",
            font=("Tahoma", 20, "bold"),
            fg="#2c3e50"
        ).pack(pady=(20, 10))


        for login in logins:
            stat_local =  [item for item in stat if item.get("login") == login]
            create_stat_block(scroll_frame.scrollable_frame, login, stat_local)

        tk.Button(
            scroll_frame.scrollable_frame,
            text="Очистить всю базу",
            font=("Tahoma", 12, "bold"),
            bg="#3498db",
            fg="white",
            width=20,
            height=2,
            command=self.clean_base,
            cursor="hand2"
        ).pack(pady=(20, 10))

    def create_user_header(self, parent_frame, user):

        header_frame = tk.Frame(parent_frame, bg="#2c3e50", height=60)
        header_frame.pack(fill="x", side="top")
        header_frame.pack_propagate(False)


        user_info_frame = tk.Frame(header_frame, bg="#2c3e50")
        user_info_frame.pack(side="left", padx=20)

        # Имя пользователя
        tk.Label(
            user_info_frame,
            text=user,
            font=("Tahoma", 14, "bold"),
            bg="#2c3e50",
            fg="white"
        ).pack(side="left", padx=(0, 10))

        # Кнопка выхода справа
        logout_button = tk.Button(
            header_frame,
            text="Выйти",
            font=("Tahoma", 11),
            bg="#e74c3c",
            fg="white",
            activebackground="#c0392b",
            activeforeground="white",
            cursor="hand2",
            command=self.logout,
            padx=20,
            pady=5
        )
        logout_button.pack(side="right", padx=20)

        return header_frame

    def logout(self):
        self.current_user = None
        self.show_login_window()

    def clean_base(self):
        answer = messagebox.askyesno("Подтверждение", "Вы уверены, что хотите очистить всю базу данных?")
        if answer:
            database.clean_base()
            self.show_login_window()
        else:
            return
