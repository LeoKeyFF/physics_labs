import tkinter as tk


class ScrollableFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__()
        self.container = tk.Frame(parent)

        self.canvas = tk.Canvas(self.container)
        self.scrollbar = tk.Scrollbar(self.container, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)

        # Создаем окно в Canvas
        self.scrollable_frame_id = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        # Настройка скроллинга
        self.scrollable_frame.bind("<Configure>", self._on_frame_configure)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Упаковка
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Привязка мыши
        self.canvas.bind("<Enter>", self._bind_to_mousewheel)
        self.canvas.bind("<Leave>", self._unbind_from_mousewheel)

    def _on_frame_configure(self, event=None):
        """Обновляем область скроллинга"""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _bind_to_mousewheel(self, event):
        """Привязываем колесико когда курсор над Canvas"""
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _unbind_from_mousewheel(self, event):
        """Отвязываем когда курсор уходит"""
        self.canvas.unbind_all("<MouseWheel>")

    def _on_mousewheel(self, event):
        """Обработка колесика мыши"""
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def pack(self, **kwargs):
        """Прокси для pack"""
        return self.container.pack(**kwargs)
