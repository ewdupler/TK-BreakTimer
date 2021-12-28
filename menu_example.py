from tkinter import *
from tkinter.ttk import *

OPTIONS = [
"Jan",
"Feb",
"Mar"
]
def Donothing():
    return

root = Tk()

hello = StringVar()
hello.set("Hello World")

message = Label(root, textvariable=hello)
message.pack()
variable = StringVar(root)
variable.set(OPTIONS[0]) # default value

menu = Menu(root)
root.config(menu=menu)
opts_menu = Menu(menu, tearoff=0)
opts_sub_menu = Menu(opts_menu, tearoff=0)

menu.add_cascade(label="Options", menu=opts_menu)
opts_menu.add_cascade(label="Colors", menu=opts_sub_menu)
opts_sub_menu.add_command(label="Do Nothing", command=Donothing)


def ok():
    print ("value is:" + variable.get())

button = Button(root, text="OK", command=ok)
button.pack()

root.bind(message)



mainloop()
