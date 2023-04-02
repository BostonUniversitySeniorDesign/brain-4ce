import tkinter as tk
import time

class Circle:
    def __init__(self, canvas):
        self.canvas = canvas
        self.draw() 

    def draw(self):
        self.canvas.delete("all")
        self.x = 45
        self.y = 25
        for i in range(6):
            
            self.canvas.create_oval(self.x, self.y, self.x+50, self.y+50, fill='white')
            self.x += 75
            
            if i == 2:
                self.y += 75
                self.x = 45

        self.canvas.scale("all", 0, 0, 2, 2)
        self.canvas.after(500, self.draw)


def tWindow():

    window = tk.Tk()
    window.title("Brain4ce Menu")

    #Set window size and pos

    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    window_width = 600
    window_height = 400
    x_pos = (screen_width - window_width) // 2
    y_pos = (screen_height - window_height) // 2

    window.geometry("{}x{}+{}+{}".format(window_width, window_height, x_pos, y_pos))

    canvas = tk.Canvas(window, width=600, height=400)
    canvas.pack()


    canvas.scale("all", 0, 0, 1.5, 1.5)
    Circle(canvas)
           

    window.mainloop()


tWindow()