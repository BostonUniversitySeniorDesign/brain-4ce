import tkinter as tk
import sys
import os


class MainMenu(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack(expand=True)
        self.create_widgets()

    def create_widgets(self):

        self.button_frame = tk.Frame(self)
        self.button_frame.pack(expand=True)

        self.button1 = tk.Button(self.button_frame, text="Run Virtual Environment", command=self.run_venv)
        self.button1.pack(side="top", pady=10)

        self.button2 = tk.Button(self.button_frame, text="Run 30s Game", command=self.run_30sgame)
        self.button2.pack(side="bottom", pady=10)

        self.button3 = tk.Button(self.button_frame, text="Run 2D Game", command=self.run_2dgame)
        self.button3.pack(side="top", pady=20)

    def run_venv(self):

        os.system("python VirtualEnvironment/main_sim.py")

    def run_2dgame(self):

        os.system("python 2DGame/main.py")

    def run_30sgame(self):
        
        os.system("python 30s\ Game/main.py")

if __name__ == '__main__':
    root = tk.Tk()

    root.title("Main Menu")

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    window_width = 300
    window_height = 200
    x_pos = (screen_width - window_width) // 2
    y_pos = (screen_height - window_height) // 2

    root.geometry("{}x{}+{}+{}".format(window_width, window_height, x_pos, y_pos))
    app = MainMenu(master=root)
    app.mainloop()

    exit(0)