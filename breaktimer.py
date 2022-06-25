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
SCHOOL = 'Neutral'
colors = {
    'Neutral': {'primary':'darkgray', 'secondary': 'white'},
    'Miami': {'primary': 'orange', 'secondary': 'white'},
    'PSU':   {'primary': 'blue',   'secondary': 'white'},
    'Michigan': {'primary': 'darkblue', 'secondary': 'yellow'},
    'NYU': {'primary': '#57068C', 'secondary': 'white'}  # purple/white
}
presetMessages = [
    "Break Time!",
    "Lab 1",
    "Lab 2",
    "Lab 3",
    "Lab 4",
    "Lab 5",
    "Lunch"
]
minutesAdd = [1, 5, 10]
minutesTotal = [1, 5, 10, 20, 30, 50]

FONT = 'Courier'
FONTSIZE = 60
DONE_MESSAGE = "TIME IS UP!"
is_sound_playing = False

starttime = dt.datetime.now()

def main():
    # message = input("Timer message (enter for none): ")
    # minutes = input("Minutes for break/or end time (HH:MM - 24hr): ")
    message = "Break Time!"
    minutes = "5"

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
        try:
            play_sound('off')
        except:
            pass


def play_sound(command='on'):
    global sound
    global is_sound_playing

    if command == 'on':
        # Loops the selected music
        sound = music.songtime()
        sound.loop()
        is_sound_playing = True
    elif command == 'alarm':
        # Stops the music and plays the alarm
        play_sound('stop')
        sound = music.songtime()
        sound.playend()
    else:
        sound.stop()
        is_sound_playing = False

def add_minutes(minutes=1):
    global timeend
    timeend = timeend + dt.timedelta(minutes=minutes)
    return

def total_minutes(minutes=1):
    global timeend
    timeend = starttime + dt.timedelta(minutes=minutes)
    timeepoch = (((int(timeend.timestamp())) + 30) // 60) * 60
    timeend = dt.datetime.fromtimestamp(timeepoch)
    return

def break_timer(minutes=1, message=""):
    timenow = starttime
    global timeend
    timeend = timenow + dt.timedelta(minutes=minutes)
    timeepoch = (((int(timeend.timestamp())) + 30) // 60) * 60
    timeend = dt.datetime.fromtimestamp(timeepoch)

    lblMessage=""

    # Set up Graphical app via TkInter
    root = Tk()
    root.title('Class Timer')
    root['bg' ] = colors[SCHOOL]['primary']

    # Do this when the break is over
    def timer_complete():
        if is_sound_playing:
            print("Sound alarm")
            play_sound('alarm')

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
        # print(colorscheme)
        return

    def setMessage(message=""):
        lblMessage.config(text=f"{message}")
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

        ## Time Add Menu
        time_menu = Menu(menu, tearoff=0)
        menu.add_cascade(label="Time", menu=time_menu)
        time_sub_menu = Menu(time_menu, tearoff=0)
        time_menu.add_cascade(label="Add", menu=time_sub_menu)
        for min in minutesAdd:
            time_sub_menu.add_command(label=f"{min} min", command=lambda c=min: add_minutes(c))
        ttot_sub_menu = Menu(time_menu, tearoff=0)
        time_menu.add_cascade(label="Total Time", menu=ttot_sub_menu)
        for min in minutesTotal:
            ttot_sub_menu.add_command(label=f"{min} min", command=lambda c=min: total_minutes(c))

        ## Message Menu
        msg_menu = Menu(menu, tearoff=0)
        menu.add_cascade(label="Message", menu=msg_menu)
        for message in presetMessages:
            msg_menu.add_command(label=f"{message}", command=lambda c=f"{message}": setMessage(c))



        return

    # Function to update the timer
    def settimelabel():
        timenow = dt.datetime.now()
        timeleft = timeend - timenow + dt.timedelta(seconds=1)
        # if timeleft.seconds > 0:
        if timeend > timenow:
            lblTimeNow.config(text=f"Now: {timenow.strftime('%I:%M:%S %p')}")
            # Set the time label
            minutes = timeleft.seconds // 60 % 60
            hours = ((timeleft.seconds // 60) - minutes) // 60

            # Format label as M:SS if less than an hour.  Otherwise HH:MM:SS
            if hours < 1:
                if int(minutes) < 1:
                    lblTimeLeft.config(text=f"Remaining: {timeleft.seconds % 60}")
                else:
                    lblTimeLeft.config(text=f"Remaining: {minutes}:{timeleft.seconds % 60:02}")
            else:
                lblTimeLeft.config(text=f"Remaining: {hours:02}:{minutes:02}:{timeleft.seconds % 60:02}")

            lblTimeEnd.config(text=f"Return: {timeend.strftime('%I:%M:%S %p')}")

            root.after(1000, settimelabel)
        else:
            root.after(1000, timer_complete)

    # Message Label
    lblMessage = Label(root, font=(FONT, int(FONTSIZE * 1.25), 'bold'),
                       background=colors[SCHOOL]['primary'],
                       foreground=colors[SCHOOL]['secondary'])
    # lblMessage.config(text=f"{message}")
    setMessage(message)
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