import tkinter as tk

def Save():
    print("Save selected")

def Cancel():
    print("Save canceled")

def savedata():

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

    canvas = tk.Canvas(window, width=300, height=200)
    canvas.pack()

    canvas.create_text(150, 50, text="Save data?", fill="black", font=('Helvetica 25 bold'))
   # canvas.place(relx=0.5, rely=0.5, anchor='n')

    bYes = tk.Button(window, text="Yes", command=Save)
    bYes.place(relx=0.4, rely=0.6, anchor="se")

    bNo = tk.Button(window, text="No", command=Cancel)
    bNo.place(relx=0.7, rely=0.6, anchor="se")
