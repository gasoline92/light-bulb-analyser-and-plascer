import tkinter as tk
import math
from tkinter import simpledialog, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
class LampPlacer:
    def __init__(self, master):
        self.master = master
        self.master.title("Оптимальное размещение ламп")
        self.room_width = 10
        self.room_length = 10
        self.room_height = 3
        self.lamp_power = 1000
        self.min_illumination = 300
        self.lamp_height = 2.5
        self.max_illumination_distance = 5
        self.illumination_angle = 160
        self.lamp_spacing_x = 0
        self.lamp_spacing_y = 0
        self.lamps_x = 0
        self.lamps_y = 0
        self.setup_ui()
        self.clear_canvas()
    def setup_ui(self):
        self.main_frame = tk.Frame(self.master)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        self.control_frame = tk.Frame(self.main_frame)
        self.control_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.Y)
        self.canvas_frame = tk.Frame(self.main_frame)
        self.canvas_frame.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH, padx=10, pady=10)
        self.create_controls()
        self.create_canvas()
    def create_controls(self):
        tk.Button(self.control_frame, text="Ввести параметры", command=self.get_parameters).pack(pady=5, fill=tk.X)
        tk.Button(self.control_frame, text="Рассчитать", command=self.calculate_placement).pack(pady=5, fill=tk.X)
        tk.Button(self.control_frame, text="Очистить", command=self.clear_canvas).pack(pady=5, fill=tk.X)
        #tk.Button(self.control_frame, text="Построить диаграмму", command=self.plot_illumination_pattern).pack(pady=5, fill=tk.X)
        self.params_frame = tk.LabelFrame(self.control_frame, text="Параметры")
        self.params_frame.pack(pady=10, fill=tk.X)
        self.info_label = tk.Label(self.control_frame, text="", justify=tk.LEFT)
        self.info_label.pack(pady=10)
    def create_canvas(self):
        self.canvas = tk.Canvas(self.canvas_frame, width=600, height=600, bg='white')
        self.canvas.pack()
        self.figure = Figure(figsize=(5, 4), dpi=100)
        self.illumination_plot = self.figure.add_subplot(111)
        self.canvas_plot = FigureCanvasTkAgg(self.figure, master=self.canvas_frame)
        self.canvas_plot.get_tk_widget().pack()
        self.canvas_plot.get_tk_widget().pack_forget()
    def get_parameters(self):
        params = [
            ("Ширина помещения (м):", self.room_width, 1, 200),
            ("Длина помещения (м):", self.room_length, 1, 200),
            ("Высота помещения (м):", self.room_height, 2, 20),
            ("Световой поток лампы (люмен):", self.lamp_power, 100, 10000),
            ("Минимальная освещенность (люкс):", self.min_illumination, 10, 10000),
            ("Высота подвеса ламп (м):", self.lamp_height, 0.2, 20),
            ("Макс. расстояние освещения (м):", self.max_illumination_distance, 1, 300),
            ("Угол освещения (градусы):", self.illumination_angle, 30, 180)
        ]
        results = []
        for text, default, minval, maxval in params:
            result = simpledialog.askfloat("Параметры", text, initialvalue=default, minvalue=minval, maxvalue=maxval)
            if result is None:
                return
            results.append(result)
        (self.room_width, self.room_length, self.room_height, 
         self.lamp_power, self.min_illumination, self.lamp_height,
         self.max_illumination_distance, self.illumination_angle) = results
    #war thunder
    def calculate_placement(self):
        try:
            working_height = self.room_height - self.lamp_height
            if working_height <= 0:
                messagebox.showerror("Ошибка", "Высота подвеса ламп должна быть меньше высоты помещения")
                return
            effective_radius = working_height * math.tan(math.radians(self.illumination_angle/2))
            spacing = min(effective_radius, self.max_illumination_distance)
            self.lamps_x = math.ceil(self.room_width / spacing)
            self.lamps_y = math.ceil(self.room_length / spacing)
            self.lamp_spacing_x = self.room_width / self.lamps_x
            self.lamp_spacing_y = self.room_length / self.lamps_y
            self.margin_x = self.lamp_spacing_x / 2
            self.margin_y = self.lamp_spacing_y / 2
            self.draw_room()
            self.plot_illumination_pattern()
            info_text = (
                f"Помещение: {self.room_width}x{self.room_length}x{self.room_height} м\n"
                f"Ламп: {self.lamps_x}x{self.lamps_y} = {self.lamps_x*self.lamps_y} шт\n"
                f"Расстояние между лампами: {self.lamp_spacing_x:.2f}x{self.lamp_spacing_y:.2f} м\n"
                f"Рабочая высота: {working_height:.2f} м\n"
                f"Эффективный радиус: {effective_radius:.2f} м\n"
                f"Угол освещения: {self.illumination_angle}°"
            )
            self.info_label.config(text=info_text)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка: {str(e)}")
    def draw_room(self):
        self.clear_canvas()
        scale_x = 550 / self.room_width
        scale_y = 550 / self.room_length
        scale = min(scale_x, scale_y)
        room_pixels_width = self.room_width * scale
        room_pixels_length = self.room_length * scale
        start_x = (600 - room_pixels_width) / 2
        start_y = (600 - room_pixels_length) / 2
        self.canvas.create_rectangle(start_x, start_y, 
                                   start_x + room_pixels_width, start_y + room_pixels_length, 
                                   outline='black', width=2)
        lamp_radius = 5
        for i in range(self.lamps_x):
            for j in range(self.lamps_y):
                x = start_x + (self.margin_x + i * self.lamp_spacing_x) * scale
                y = start_y + (self.margin_y + j * self.lamp_spacing_y) * scale
                self.canvas.create_oval(x - lamp_radius, y - lamp_radius, 
                                      x + lamp_radius, y + lamp_radius, 
                                      fill='yellow', outline='black')
                radius = min(self.max_illumination_distance, 
                            (self.room_height - self.lamp_height) * 
                            math.tan(math.radians(self.illumination_angle/2))) * scale
                self.canvas.create_oval(x - radius, y - radius, 
                                      x + radius, y + radius, 
                                      outline='gray', dash=(2,2))
        self.canvas.create_text(start_x + room_pixels_width/2, start_y-10, 
                              text=f"{self.room_width} м", anchor=tk.N)
        self.canvas.create_text(start_x-10, start_y+room_pixels_length/2, 
                              text=f"{self.room_length} м", anchor=tk.E)
    def plot_illumination_pattern(self):
        self.illumination_plot.clear()
        working_height = self.room_height - self.lamp_height
        max_dist = self.max_illumination_distance
        angle = math.radians(self.illumination_angle)
        distances = [d * 0.1 for d in range(0, int(max_dist*10)+1)]
        i = []
        for d in distances:
            if d == 0:
                e = self.lamp_power
            else:
                angle_at_dist = math.atan2(d, working_height)
                if angle_at_dist > angle/2:
                    e = 0
                else:
                    e = self.lamp_power * math.cos(angle_at_dist) / (working_height**2 + d**2)
            i.append(e)
        self.illumination_plot.plot(distances, i)
        self.illumination_plot.set_title("Диаграмма освещенности лампы")
        self.illumination_plot.set_xlabel("Расстояние от лампы (м)")
        self.illumination_plot.set_ylabel("Освещенность (люкс)")
        self.illumination_plot.grid(True)
        self.canvas_plot.get_tk_widget().pack()
        self.canvas_plot.draw()
    def clear_canvas(self):
        self.canvas.delete("all")
        self.canvas.create_text(300, 300, 
                               text="Введите параметры помещения и нажмите 'Рассчитать'", 
                               fill="gray", font=("Arial", 12))
        self.canvas_plot.get_tk_widget().pack_forget()
if __name__ == "__main__":
    root = tk.Tk()
    app = LampPlacer(root)
    root.mainloop()