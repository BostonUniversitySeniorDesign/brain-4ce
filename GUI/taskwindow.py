import tkinter as tk
import time

class Circle:
    def __init__(self, canvas, x, y):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.radius = 50
        self.color_index = 0
        self.colors = ["red", "white"]
        self.draw()

    def draw(self):
        self.canvas.delete("all")
        for i in range(1):
            color = self.colors[(self.color_index+i)%len(self.colors)]
            #x = self.x + i * 120 - 60
            self.canvas.create_oval(self.x, self.y, self.x+50, self.y+50, fill=color)
        self.color_index = (self.color_index + 1) % len(self.colors)
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

    canvas = tk.Canvas(window, width=450, height=450)
    canvas.pack()

    # ovals = []

    # ovals.append(canvas.create_oval(25, 25, 75, 75, outline='black', width=2))
    # ovals.append(canvas.create_oval(100, 25, 150, 75, outline='black', width=2))
    # ovals.append(canvas.create_oval(175, 25, 225, 75, outline='black', width=2))
    # ovals.append(canvas.create_oval(25, 100, 75, 150, outline='black', width=2))
    # ovals.append(canvas.create_oval(100, 100, 150, 150, outline='black', width=2))
    # ovals.append(canvas.create_oval(175, 100, 225, 150, outline='black', width=2))

    circle1 = Circle(canvas, 25, 75)
    # circle2 = Circle(canvas, 100, 25)
    # circle3 = Circle(canvas, 0, 0)
    # circle4 = Circle(canvas, 25, 100)
    # circle5 = Circle(canvas, 100, 100)
    # circle6 = Circle(canvas, 175, 100)

    canvas.scale("all", 0, 0, 2, 2)
    # canvas.place(relx=0.45, rely=0.05, anchor='n')
    # canvas.create_text(100, 100, text="1", fill="black", font=('Helvetica 25 bold'))
    # canvas.create_text(250, 100, text="2", fill="black", font=('Helvetica 25 bold'))   
    # canvas.create_text(400, 100, text="3", fill="black", font=('Helvetica 25 bold'))
    # canvas.create_text(100, 250, text="4", fill="black", font=('Helvetica 25 bold'))
    # canvas.create_text(250, 250, text="5", fill="black", font=('Helvetica 25 bold'))
    # canvas.create_text(400, 250, text="6", fill="black", font=('Helvetica 25 bold'))            

    window.mainloop()
