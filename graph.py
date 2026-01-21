class Graph():
    def __init__(self, canvas, width, line_list, Vmax):
        super().__init__()
        self.line = None
        self.canvas = canvas
        self.list = []
        self.width = width
        self.line_list = line_list
        self.show = False
        self.type = "y"
        self.Vmax = Vmax

    def delete(self):
        for g in self.list:
            self.canvas.delete(g)

    def draw(self):
        # gr_x, gr_y = 800, 100
        # gr_x2, gr_y2 = 800, 300
        # gr_x3, gr_y3 = 800, 200
        # g1 = self.canvas.create_rectangle(gr_x - 50, gr_y - 60, self.width, gr_y2 + 60, fill="white")
        # self.list.append(g1)
        # g2 = self.canvas.create_rectangle(gr_x - 40, gr_y - 50, self.width, gr_y2 + 50)
        # self.list.append(g2)
        # g3 = self.canvas.create_line(gr_x, gr_y - 50, gr_x2, gr_y2 + 50, width=2)
        # self.list.append(g3)
        # g4 = self.canvas.create_line(gr_x - 40, gr_y3, self.width, gr_y3, width=2)
        # self.list.append(g4)

        x_left = 750
        border = 10
        x_start = 800
        y_top= 40
        y_bottom = 360
        y_middle = 200

        height = y_bottom - y_top - 2 * border
        w_size = self.width - x_start

        g1 = self.canvas.create_rectangle(x_left, y_top, self.width, y_bottom, fill="white")
        self.list.append(g1)
        g2 = self.canvas.create_rectangle(x_left + border, y_top + border, self.width, y_bottom - border)
        self.list.append(g2)
        g3 = self.canvas.create_line(x_start, y_top + border, x_start, y_bottom - border, width=2)
        self.list.append(g3)
        g4 = self.canvas.create_line(x_left + border, y_middle, self.width, y_middle, width=2)
        self.list.append(g4)
        for k in range(1, 11, 1):
            g5 = self.canvas.create_line((x_start + k * w_size/10, y_middle + 5), (x_start + k * w_size/10, y_middle - 5), width=3)
            self.list.append(g5)
            g6 = self.canvas.create_text(x_start + k * w_size/10, y_middle + 20, text=str(k), font='Constantia 8')
            self.list.append(g6)
        for k in range(-5, 6 , 1):
            g7 = self.canvas.create_line((x_start - 5, y_middle - k * (height/2) / 6 ), (x_start + 5, y_middle - k * (height/2) / 6), width=3)
            self.list.append(g7)
            g8 = self.canvas.create_text(x_start - 20, y_middle - k * (height/2) / 6 , text=str(int(self.Vmax * k / 5)), font='Constantia 8')
            self.list.append(g8)
        g9 = self.canvas.create_text(x_start + 30, y_top + 20, text =  'Vx(м/с)' if self.type == "x" else 'Vy(м/с)', font='Constantia 8')
        self.list.append(g9)
        g10 = self.canvas.create_text(self.width - 20, y_middle - 20, text='t(с)', font='Constantia 8')
        self.list.append(g10)

    def draw_line(self):
        if len(self.line_list)>0:
            self.line = self.canvas.create_line(self.line_list)
        self.list.append(self.line)

    def delete_line(self):
        self.canvas.delete(self.line)
