import tkinter as tk
import savewindow

class Circle:
    def __init__(self, canvas, window):
        self.window = window
        self.canvas = canvas
        self.iswhite = True
        self.curr = 0
        self.labels = ['Right arm!', 'Left arm!', 'Right foot!', 'Left foot!', 'Left hand!', 'Right hand!']
        self.draw()
        
    def erase_text(self):

        if self.curr != 6:
            self.canvas.delete("all")
            self.canvas.after(2000, self.draw)

    def draw(self):
        self.x = 45
        self.y = 25
        self.circles = []

        self.canvas.scale("all", 0, 0, 2, 2)

        self.change_task()

        self.canvas.after(5000, self.erase_text)

        
    def change_task(self):

        self.canvas.create_text(300, 185, text=self.labels[self.curr], fill="black", font=('Calibri 60 bold'))
        self.curr = self.curr + 1
        if self.curr == 6:
            self.window.destroy()
            savewindow.savedata()
            return


def tWindow():
    window = tk.Tk()
    window.title("Brain4ce Menu")

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


