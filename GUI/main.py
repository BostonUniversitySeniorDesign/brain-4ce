import tkinter as tk
import taskwindow

def StartImagery():
    print("bImg selected")

def StartReal():
    window.destroy()
    print("real selected")
    taskwindow.tWindow()


window = tk.Tk()
window.title("Brain4ce Menu")

#Set window size and pos

screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
window_width = 300
window_height = 200
x_pos = (screen_width - window_width) // 2
y_pos = (screen_height - window_height) // 2

window.geometry("{}x{}+{}+{}".format(window_width, window_height, x_pos, y_pos))

users = ['User 1', 'User 2', 'User 3', 'User 4', 'User 5']
variable = tk.StringVar(window)
variable.set(users[0])

dUsers = tk.OptionMenu(window, variable, *users)
dUsers.configure(background="white", activebackground="white")
dUsers["menu"].configure(bg="white")
#dUsers.pack()
dUsers.place(relx=0.5, rely=0.05, anchor='n')

bStartImg = tk.Button(window, text="Start Imagery", command=StartImagery)
bStartImg.place(relx=0.4, rely=0.5, anchor="se")

bStartReal = tk.Button(window, text="Start Real", command=StartReal)
bStartReal.place(relx=0.8, rely=0.5, anchor = "se")



window.mainloop()
