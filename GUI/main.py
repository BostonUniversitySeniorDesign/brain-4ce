import tkinter as tk
import taskwindow


class MainGUI:
    def StartImagery(self):
        print("bImg selected")

    def StartReal(self):
        self.window.destroy()
        print("real selected")
        taskwindow.tWindow()

    def __init__(self):

        self.window = tk.Tk()
        self.window.title("Brain4ce Menu")

        #Set window size and pos

        self.screen_width = self.window.winfo_screenwidth()
        self.screen_height = self.window.winfo_screenheight()
        self.window_width = 300
        self.window_height = 200
        self.x_pos = (self.screen_width - self.window_width) // 2
        self.y_pos = (self.screen_height - self.window_height) // 2

        self.window.geometry("{}x{}+{}+{}".format(self.window_width, self.window_height, self.x_pos, self.y_pos))

        users = ['User 1', 'User 2', 'User 3', 'User 4', 'User 5']
        variable = tk.StringVar(self.window)
        variable.set(users[0])

        dUsers = tk.OptionMenu(self.window, variable, *users)
        dUsers.configure(background="white", activebackground="white")
        dUsers["menu"].configure(bg="white")
        #dUsers.pack()
        dUsers.place(relx=0.5, rely=0.05, anchor='n')

        bStartImg = tk.Button(self.window, text="Start Imagery", command=self.StartImagery)
        bStartImg.place(relx=0.4, rely=0.5, anchor="se")

        bStartReal = tk.Button(self.window, text="Start Real", command=self.StartReal)
        bStartReal.place(relx=0.8, rely=0.5, anchor = "se")

        self.window.mainloop()


main = MainGUI()

