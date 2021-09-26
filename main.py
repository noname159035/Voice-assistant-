from tkinter import *
from PIL import ImageTk,Image
import time
from Sanya_helper import start


def go():
    # btn.place_forget()
    # btn2.place(x=150, y=165)
    #
    # text.place(x=45, y=30)
    #
    # time.sleep(3)

    start(window, text)

def stop():
    window.destroy()
    exit(0)


window = Tk()
window.title("ALEX")
window.geometry('400x250')
window.resizable(width=False, height=False)
window['bg'] = "#3191BB"

background_image = Image.open("img.png")
image1 = ImageTk.PhotoImage(background_image)
background_label = Label(window, image=image1)
background_label.place(x=-2, y=-2)

# lbl = Label(window, text="A L E X", font=("Impact", 40))
# lbl.place(x=100, y=50)

# btn = Button(window, text="ЗАПУСК", command=go, font=60)
# btn.place(x=150, y=100)

btn2 = Button(window, text="ВЫХОД", command=stop, font=60)
btn2.place(x=150, y=165)

text = Text(window, width=38, height=7)
text.place(x=45, y=30)

go()

# while btn['state'] != "disabled":
#     window.update()