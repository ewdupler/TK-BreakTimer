# importing whole module
from tkinter import *
from tkinter.ttk import *

import sys
import datetime as dt

# Only play music if the module exists for import
try:
    import music
    playmusic = True
except ImportError:
    playmusic = False


# Global Variables
SCHOOL = 'Miami'
colors = {
    'Miami': {'primary': 'orange', 'secondary': 'white'},
    'PSU':   {'primary': 'blue',   'secondary': 'white'},
    'Michigan': {'primary': 'darkblue', 'secondary': 'yellow'},
    'NYU': {'primary': '#57068C', 'secondary': 'white'}  # purple/white
}
FONT = 'Courier'
FONTSIZE = 60
DONE_MESSAGE = "TIME IS UP!"

def main():
    message = input("Timer message (enter for none): ")
    minutes = input("Minutes for break/or end time (HH:MM - 24hr): ")
    try:
        if ":" in minutes:
            # If a time is given, convert it to minutes instead.
            timeparts = minutes.split(":")
            endtime = dt.datetime.now().replace(hour=int(timeparts[0]), minute=int(timeparts[1]), second=int(0))
            # endtime = dt.datetime.now().replace(hour=int(timeparts[0]), minute=0, second=int(0))
            timediff = endtime - dt.datetime.now()
            minutes = timediff.seconds / 60
            if minutes < 0:
                print("You must use a time in the future")
                sys.exit(1)
        elif minutes.isnumeric():
            minutes = int(minutes)
        else:
            print("Invalid input")
            sys.exit(1)
    except Exception as e:
        print(f"Error detected: {e}")
        sys.exit(1)

    # Uncomment to default to starting with music
    # if playmusic:
    #     play_sound()

    break_timer(minutes, message)

    if playmusic:
        play_sound('off')

def play_sound(command='on'):
    global sound

    if command == 'on':
        sound = music.songtime()
        sound.loop()
    else:
        sound.stop()

def break_timer(minutes=1, message=""):
    timenow = dt.datetime.now()
    timeend = timenow + dt.timedelta(minutes=minutes)

    # Set up Graphical app via TkInter
    root = Tk()
    root.title('Class Timer')
    root['bg' ] = colors[SCHOOL]['primary']

    # Do this when the break is over
    def timer_complete():
        root['bg'] = 'red'
        lblMessage.config(background="red",
                          foreground="white")
        lblTimeNow.config(text=f"Now: {timeend.strftime('%I:%M:%S %p')}",
                            background = "red",
                            foreground = "white")
        lblTimeLeft.config(text=f"{DONE_MESSAGE}",
                            background = "red",
                            foreground = "white")
        lblTimeEnd.config(text=f"Return: {timeend.strftime('%I:%M:%S %p')}",
                            background = "red",
                            foreground = "white")

    def change_color(colorscheme):
        global SCHOOL
        SCHOOL = colorscheme
        if colorscheme:
            root['bg'] = colors[SCHOOL]['primary']
            lblMessage.config(
                background=colors[SCHOOL]['primary'],
                foreground=colors[SCHOOL]['secondary'])
            lblTimeNow.config(
                background=colors[SCHOOL]['primary'],
                foreground=colors[SCHOOL]['secondary'])
            lblTimeLeft.config(
                background=colors[SCHOOL]['primary'],
                foreground=colors[SCHOOL]['secondary'])
            lblTimeEnd.config(
                background=colors[SCHOOL]['secondary'],
                foreground=colors[SCHOOL]['primary'])
        print(colorscheme)
        return

    def makemenu():

        menu = Menu(root)
        root.config(menu=menu)

        ## Options Submenu
        opts_menu = Menu(menu, tearoff=0)
        opts_sub_menu = Menu(opts_menu, tearoff=0)

        menu.add_cascade(label="Options", menu=opts_menu)
        opts_menu.add_cascade(label="Color Scheme", menu=opts_sub_menu)

        for colorscheme in colors:
            opts_sub_menu.add_command(label=f"{colorscheme}", command=lambda c=colorscheme: change_color(c))

        ## Sound Submenu
        # sound_menu = Menu(menu, tearoff=0)
        sound_sub_menu = Menu(opts_sub_menu, tearoff=0)
        opts_menu.add_cascade(label="Sound", menu=sound_sub_menu)
        sound_sub_menu.add_command(label="On",  command=lambda c='on': play_sound(c))
        sound_sub_menu.add_command(label="Off", command=lambda c='off': play_sound(c))

        return

    # Function to update the timer
    def settimelabel():
        timenow = dt.datetime.now()
        timeleft = timeend - timenow
        if timeleft.seconds > 0:
            lblTimeNow.config(text=f"Now: {timenow.strftime('%I:%M:%S %p')}")
            lblTimeLeft.config(text=f"Remaining: {timeleft.seconds}s")
            lblTimeEnd.config(text=f"Return: {timeend.strftime('%I:%M:%S %p')}")

            root.after(1000, settimelabel)
        else:
            root.after(1000, timer_complete)

    # Message Label
    lblMessage = Label(root, font=(FONT, int(FONTSIZE * 1.25), 'bold'),
                       background=colors[SCHOOL]['primary'],
                       foreground=colors[SCHOOL]['secondary'])
    lblMessage.config(text=f"{message}")
    if message != "":
        # Only display the message if it was specified
        lblMessage.pack(anchor='center')


    # Defining and creating each label
    # Current Time Label
    lblTimeNow = Label(root, font=(FONT, FONTSIZE, 'bold'),
                background=colors[SCHOOL]['primary'],
                foreground=colors[SCHOOL]['secondary'])
    lblTimeNow.pack(anchor='center')

    # Time Left Label
    lblTimeLeft = Label(root, font=(FONT, FONTSIZE, 'bold'),
                background=colors[SCHOOL]['primary'],
                foreground=colors[SCHOOL]['secondary'])
    lblTimeLeft.pack(anchor='center')

    # Target Tim eLabel
    lblTimeEnd = Label(root, font=(FONT, FONTSIZE, 'bold'),
                background=colors[SCHOOL]['secondary'],
                foreground=colors[SCHOOL]['primary'])
    lblTimeEnd.pack(anchor='center')

    # Set the initial label times.
    settimelabel()
    makemenu()
    root.after(1000, settimelabel)
    mainloop()


if __name__ == "__main__":
    main()