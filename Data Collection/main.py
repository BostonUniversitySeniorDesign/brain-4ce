import tkinter as tk
import taskwindow
import find_cyton

class MainGUI:
    def StartImagery(self):
        self.window.destroy()
        taskwindow.tWindow(self.board, 'i')
        
    def StartReal(self):
        self.window.destroy()
        taskwindow.tWindow(self.board, 'r')

    def __init__(self):

        self.window = tk.Tk()
        self.window.title("Brain4ce Menu")


        self.screen_width = self.window.winfo_screenwidth()
        self.screen_height = self.window.winfo_screenheight()
        self.window_width = 300
        self.window_height = 200
        self.x_pos = (self.screen_width - self.window_width) // 2
        self.y_pos = (self.screen_height - self.window_height) // 2

        self.window.geometry("{}x{}+{}+{}".format(self.window_width, self.window_height, self.x_pos, self.y_pos))

        bStartImg = tk.Button(self.window, text="Start Imagery", command=self.StartImagery)
        bStartImg.place(relx=0.4, rely=0.5, anchor="se")

        bStartReal = tk.Button(self.window, text="Start Real", command=self.StartReal)
        bStartReal.place(relx=0.95, rely=0.5, anchor = "se")

        self.board = find_cyton.find_cyton(lambda x : True)
        self.board.prepare_session()



        self.window.mainloop()


main = MainGUI()

