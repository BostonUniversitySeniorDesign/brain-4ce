import tkinter as tk

class Circle:
    def __init__(self, canvas, window):
        self.window = window
        self.canvas = canvas
        self.iswhite = True
        self.curr = 0
        self.draw()
        
    def draw(self):
        self.canvas.delete("all")
        self.x = 45
        self.y = 25
        self.circles = []
        for i in range(6):
            circle = self.canvas.create_oval(self.x, self.y, self.x+50, self.y+50, fill='white')
            self.circles.append(circle)
            self.x += 75
            
            if i == 2:
                self.y += 75
                self.x = 45

        self.canvas.scale("all", 0, 0, 2, 2)

        if self.iswhite == True:
            self.change_color()
            self.iswhite = False
        else:
            self.change_color()
            self.iswhite = True

        self.canvas.after(1000, self.draw)


        
    def change_color(self):
        self.canvas.itemconfig(self.circles[self.curr], fill='red')
        self.curr = self.curr + 1
        if self.curr == 6:
            self.curr = 0


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
    Circle(canvas, window)

    window.mainloop()

tWindow()
