"""
2021-12-28 - E. Dupler - Added exit to "ok()"
                       - Changed options for menu
                       - Reformatted menu
                       - Configured with functions
"""
from tkinter import *
import tkinter.messagebox

hello = None
root = None
message = None

def main():
    global root

    root = Tk()

    make_menu(root)
    make_message_label(root)

    button = tkinter.Button(root, text="OK", command=ok)
    button.pack()

    mainloop()


def make_message_label(root):
    global hello
    global message
    hello = StringVar()
    hello.set("Hello World")
    message = tkinter.Label(root, textvariable=hello)
    message.pack()
    root.bind(message)


def make_menu(root):
    """
    Create Menu
    """
    menu = Menu(root)
    root.config(menu=menu)
    root.geometry("500x200")
    # Program Menu
    program_menu = Menu(menu, tearoff=0)
    menu.add_cascade(label="Program", menu=program_menu)
    program_menu.add_command(label="Exit", command=lambda: root.destroy())
    # Options Menu
    opts_menu = Menu(menu, tearoff=0)
    opts_sub_menu = Menu(opts_menu, tearoff=0)
    menu.add_cascade(label="Options", menu=opts_menu)
    opts_menu.add_cascade(label="Colors", menu=opts_sub_menu)
    # Options submenu
    opts_sub_menu.add_command(label='Miami', command=lambda: set_colors('orange', 'green'))
    opts_sub_menu.add_command(label='Michigan', command=lambda: set_colors('blue', 'yellow'))
    opts_sub_menu.add_command(label='PSU', command=lambda: set_colors('blue', 'white'))


def ok():
    print("value is:" + hello.get())
    root.destroy()


def set_colors(bgcolor, fgcolor):
    """ This code will set the background color of the root window. """
    global message
    global hello
    root['bg'] = bgcolor
    message.config(bg=bgcolor, fg=fgcolor)
    return


if __name__ == "__main__":
    main()
