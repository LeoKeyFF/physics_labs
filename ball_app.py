import random
import tkinter as tk

from PIL import ImageTk, Image

from aim import Aim
from ball import Ball
from ballistics import Ballistics
from graph import Graph


class BallApp(tk.Toplevel):
    def __init__(self):
        super().__init__()
        # --------- Design frames----------------------------------------------
        self.title("Бросание тела")
        self.width = 1000
        self.height = 600
        self.t = 0
        self.x0 = 100
        self.y0 = 500
        self.meter = 10

        self.num_v0 = tk.IntVar()
        self.num_alpha = tk.IntVar()
        self.num_v0.set(20)
        self.num_alpha.set(30)

        self.start = False
        self.FALSE_im = None
        self.FALSE = None
        self.OK = None
        self.OK_im = None

        self.count = 0
        self.oval_list = []

        self.v_y_list = []
        self.v_x_list = []

        #grafic show/hide button
        self.click = False

        self.button_graph_y = None
        self.in_but_graph_y = False
        self.but_rec_graph_y = [960, 360, 1000, 400]
        self.button_graph_x = None
        self.in_but_graph_x = False
        self.but_rec_graph_x = [960, 400, 1000, 440]
        self.button_graph_close = None
        self.in_but_graph_close = False
        self.but_rec_graph_close = [710, 50, 750, 90]

        self.geometry(f'{self.width+250}x{self.height + 100}')
        self.resizable(True, False)
        self.canvas = tk.Canvas(self, bg='white',width=self.width, height=self.height)
        self.canvas.grid(column=0, row=0, sticky=tk.NSEW, pady=5, padx=5, columnspan=10, rowspan = 10)

        self.graph = Graph(self.canvas, self.width, self.v_y_list)

        x0p, y0p = self.meter2pixel(0, 0)
        self.ball = Ball(x0p, y0p, self.canvas)

        x, y = self.set_aim_cords()
        self.aim = Aim(x, y, self.canvas)

        self.draw_background()
        self.draw_cords_axes()

        self.ball.draw()
        self.aim.draw()

        self.action()

        self.lab1 = tk.Label(self, text='Начальная скорость:', font=("Tahoma", 13), width=19)
        self.lab1.grid(row=10, column=0, sticky=tk.NW)

        self.entry1 = tk.Entry(self, width=10, textvariable=self.num_v0, font=("Tahoma", 13))
        self.entry1.grid(row=10, column=1, sticky=tk.NW)

        self.lab2 = tk.Label(self, text='Угол:', font=("Tahoma", 13), width=5)
        self.lab2.grid(row=11, column=0, sticky=tk.NW)

        self.entry2 = tk.Entry(self, width=10, textvariable=self.num_alpha, font=("Tahoma", 13))
        self.entry2.grid(row=11, column=1, sticky=tk.NW)

        self.lab3 = tk.Label(self, text='(НЕ должно превышать "25")', font=("Tahoma", 13), width=25)
        self.lab3.grid(row=10, column=2, sticky=tk.NW)

        self.lab3 = tk.Label(self, text='Задача:', font=("Tahoma", 13))
        self.lab3.grid(row=0, column=10, sticky=tk.SW)

        self.lab3 = tk.Label(self, wraplength=220, text='Текст задачи, где говориться, '
                                        'что ученику надо выполнить, чтобы получить правильный ответ', font='Constantia 12', justify="left")
        self.lab3.grid(row=1, column=10, sticky=tk.NW, rowspan = 2)

        self.lab3 = tk.Label(self, text='Дано:', font=("Tahoma", 13))
        self.lab3.grid(row=3, column=10, sticky=tk.SW)

        aimx, aimy = self.pixel2meter(self.aim.x, self.aim.y)
        self.lab3 = tk.Label(self, text='Центр мишени:\n' + '(x=' + str(round(aimx)) + '; y=' + str(round(aimy))+ ')', font='Constantia 12')
        self.lab3.grid(row=4, column=10, sticky=tk.NW)

        self.bind('<KeyPress>', self.key_press)
        self.bind('<Button-1>', self.mouse_click)
        self.bind('<Motion>', self.mouse_move)
        self.bind('<ButtonRelease-1>', self.mouse_release)

    def action(self):
        if not self.start:
            self.t = 0
            self.after(300, lambda: self.action())
            return

        if self.ball.V0 > self.ball.Vmax:
            self.start = False
            self.after(300, lambda: self.action())
            return

        ballx, bally = Ballistics.calc_cords(self.t, self.ball.V0, self.ball.alpha)

        if bally < 0:
            bally = 0
            self.FALSE_im = ImageTk.PhotoImage(Image.open('images/FALSE.png'))
            self.FALSE = self.canvas.create_image(self.width/2, self.height/2, image=self.FALSE_im)
            self.start = False

        xp, yp = self.meter2pixel(ballx, bally)

        if self.collision(xp, yp - self.ball.size, self.ball.size, self.ball.size, self.aim.x, self.aim.y-self.aim.height/2, self.aim.width, self.aim.height):
            self.OK_im = ImageTk.PhotoImage(Image.open('images/OK.png'))
            self.OK = self.canvas.create_image(self.width/2, self.height/2, image=self.OK_im)
            self.start = False

        self.ball.move(xp, yp)

        # draw path
        if round(xp, 0) in range(100, 100 + 80*self.meter, 1):
            self.count += 1
        if self.count in range(0, 800, 10):
            oval = self.canvas.create_oval(xp+3, yp - 20+3, xp+ 7+3, yp - 20+3 + 7, fill = 'grey', outline = "grey")
            self.oval_list.append(oval)

        # draw velocity graph
        v_y = Ballistics.calc_velocity_y(v0=self.ball.V0, t=self.t, alpha=self.ball.alpha)
        self.v_y_list.append((800 + self.t * 30, 200 - (v_y * 5)))

        v_x = Ballistics.calc_velocity_x(v0=self.ball.V0, alpha=self.ball.alpha)
        self.v_x_list.append((800 + self.t * 30, 200 - (v_x * 5)))

        self.graph.delete_line()
        if len(self.v_y_list) > 1:
            if self.graph.show:
                if self.graph.type == "y":
                    self.graph.line_list = self.v_y_list
                elif self.graph.type == "x":
                    self.graph.line_list = self.v_x_list
                self.graph.draw_line()
        self.t += 0.03
        self.after(30, lambda: self.action())


    def collision(self, x1, y1, w1, h1, x2, y2, w2, h2):
        if x1 <= x2 + w2 and x1 + w1 >= x2 and y1 + h1 >= y2 and y1 <= y2 + h2:
            return True


    def draw_background(self):
        width_m = int(self.width / self.meter)
        height_m = int(self.height / self.meter)

        for i in range(10, width_m - 15, 10):
            self.canvas.create_line((self.x0 + i * self.meter, 0), (self.x0 + i * self.meter, self.height), fill="#D3D3D3", width=3)
            self.canvas.create_text(self.x0 + i * self.meter, self.y0 + 25, text=str(int(i)), font='Constantia 20')
        for i in range(10, height_m - 10, 10):
            self.canvas.create_line((0, self.y0 - i * self.meter), (self.width, self.y0 - i * self.meter), fill="#D3D3D3", width=3)
            self.canvas.create_text(self.x0 + 25, self.y0 - i * self.meter, text=str(int(i)), font='Constantia 20')

        self.canvas.create_polygon((self.width - 20, self.y0 - 10), (self.width, self.y0), (self.width - 20, self.y0 + 10))
        self.canvas.create_polygon((self.x0 - 10, 20), (self.x0, 0), (self.x0 + 10, 20))
        self.canvas.create_text(self.x0 - 40, 30, text='y(м)', font='Constantia 20')
        self.canvas.create_text(self.width - 30, self.y0 + 40, text='x(м)', font='Constantia 20')

        self.button_graph_y = self.canvas.create_rectangle(self.but_rec_graph_y)
        self.button_graph_x = self.canvas.create_rectangle(self.but_rec_graph_x)

    def draw_cords_axes(self):
        self.canvas.create_line(0, self.y0, self.width, self.y0, width=4)
        self.canvas.create_line(self.x0, 0, self.x0, self.height, width=4)

        width_m = int(self.width / self.meter)
        height_m = int(self.height / self.meter)

        for i in range(10, width_m, 10):
            self.canvas.create_line((self.x0 + i * self.meter, self.y0 + 10), (self.x0 + i * self.meter, self.y0 - 10), width=3)
        for i in range(10, height_m, 10):
            self.canvas.create_line((self.x0 + 10, self.y0 - i * self.meter), (self.x0 - 10, self.y0 - i * self.meter), width=3)


    def meter2pixel(self, x, y):
        x = self.meter * x + self.x0
        y = self.y0 - self.meter * y
        return x, y

    def pixel2meter(self, x, y):
        x = (x - self.x0) / self.meter
        y = (self.y0 - y) / self.meter
        return x, y

    def key_press(self, event):
        if event.keysym == 'Return':
            try:
                self.ball.V0 = int(self.num_v0.get())
                self.ball.alpha = int(self.num_alpha.get())
                self.start = True
                self.v_y_list.clear()
                self.v_x_list.clear()

                if len(self.oval_list) > 0:
                    self.count = 0
                    for i in self.oval_list:
                        self.canvas.delete(i)

            except Exception as e:
                self.ball.V0 = 25
                self.ball.alpha = 30
            if self.OK:
                self.canvas.delete(self.OK)
            if self.FALSE:
                self.canvas.delete(self.FALSE)

    def set_aim_cords(self):
        x1 = random.randint(20, 70)
        y1 = random.randint(5, 30)
        y_max = Ballistics.calc_max_aim_y(x1, self.ball.Vmax)
        if y1 > y_max:
            return self.set_aim_cords()
        return self.meter2pixel(int(x1/5)*5, (int(y1/5)*5))

    def mouse_move(self, event):
        if self.find_collision(event.x, event.y, *self.but_rec_graph_y):
            self.in_but_graph_y = True
        else:
            self.in_but_graph_y = False

        if self.find_collision(event.x, event.y, *self.but_rec_graph_x):
            self.in_but_graph_x = True
        else:
            self.in_but_graph_x = False

        if self.find_collision(event.x, event.y, *self.but_rec_graph_close):
            self.in_but_graph_close = True
        else:
            self.in_but_graph_close = False


    def mouse_click(self, event):
        if self.in_but_graph_y and event:
            self.graph.type = "y"
            self.graph.line_list = self.v_y_list
            self.graph.show = True
            self.graph.draw()
            self.canvas.delete(self.button_graph_close)
            self.button_graph_close = self.canvas.create_rectangle(self.but_rec_graph_close)
            if self.OK:
                self.canvas.lift(self.OK)
            if self.FALSE:
                self.canvas.lift(self.FALSE)
            self.graph.draw_line()

        if self.in_but_graph_x and event:
            self.graph.type = "x"
            self.graph.line_list = self.v_x_list
            self.graph.show = True
            self.graph.draw()
            self.canvas.delete(self.button_graph_close)
            self.button_graph_close = self.canvas.create_rectangle(self.but_rec_graph_close)
            if self.OK:
                self.canvas.lift(self.OK)
            if self.FALSE:
                self.canvas.lift(self.FALSE)
            self.graph.draw_line()

        if self.in_but_graph_close and event:
            self.graph.show = False
            self.graph.delete()
            self.canvas.delete(self.button_graph_close)

        self.in_but_graph_y = False
        self.in_but_graph_x = False
        self.in_but_graph_close = False

        if event:
            self.click = True

    def mouse_release(self, event):
        if event:
            self.click = False

    def find_collision(self, x, y, x1, y1, x2, y2):
        if x1 < x < x2 and y1 < y < y2:
            return True


