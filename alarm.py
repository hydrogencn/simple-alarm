# Alarm clock program - Written by Rob Apr 2017
# Instructions: The alarm clock has two modes: 'Nap this long' and 'Nap until'
# To use 'Nap this long' mode enter the number of hours, minutes, and seconds you want to nap.
# then enter the filename of the song/alarm you want to use in the 'song' field. It is important
# that the song you use for the alarm is in the same directory as the alarm script.
# after all the options are set hit 'Nap this long' and your computer's default program will
# open the song file specified as if you double-clicked on it.
# To use 'Nap until' select a time you want to wake up, fill in the song you want to use,
# and hit nap until.
# The snooze function can be used after using either of the two previous modes and will
# wait ten minutes then play the alarm song again
# If url is selected a firefox window will open the browser to the link given. It does not
# necessarily have to be a youtube link.

import os
import time
import subprocess
import sys
from appJar import gui
import webbrowser


# portable file open method. first works on windows, second on linux/mac
def open_file(filename):
    if sys.platform == "win32":
        os.startfile(filename)
    else:
        opener = "open" if sys.platform == "darwin" else "xdg-open"
        subprocess.call([opener, filename])


# defining buttons.
def press(btn):
    # This button gets numbers from the hours,min,seconds fields of the gui and converts them
    # to seconds and sleeps for that long. The try/except chain allows the user to leave fields
    # blank while defaulting them to 0
    if btn == 'Nap this long':
        try:
            secnap = int(app.getEntry('sec'))
        except:
            secnap = 0
        try:
            minnap = (int(app.getEntry('min')) * 60)
        except:
            minnap = 0
        try:
            hrnap = (int(app.getEntry('hrs')) * 3600)
        except:
            hrnap = 0
        naptime = secnap + minnap + hrnap
        time.sleep(naptime)
        # Decides whether to open local file or url here
        if app.getOptionBox('alarmtype') == 'Local Song':
            open_file(app.getEntry('alarmsound'))
        else:
            # done in three lines to attempt giving your adblocker time to block ads?
            webbrowser.get('firefox')
            webbrowser.open()
            webbrowser.open_new(app.getEntry('alarmsound'))

    elif btn == 'Nap until':
        # This button gets the time now and stores it in HH:MM format.
        minsPassed = 0
        hrsPassed = 0
        timeNow = time.time()
        timeData = time.localtime(timeNow)
        nowHr = timeData.tm_hour
        nowMin = timeData.tm_min
        futureHr = int(app.getOptionBox('Time'))
        futureMin = int(app.getOptionBox('mintime'))
        # Converts 12 hour time to 24 hour time for easier calculations
        if app.getOptionBox('ampm') == 'PM' and str(futureHr) != '12':
            futureHr = futureHr + 12
        if app.getOptionBox('ampm') == 'AM' and str(futureHr) == '12':
            futureHr = 0

        # This while loop simply counts the number of minutes from now to the time
        # the user wishes to wake up. hours and minutes are incremented until both match up
        # when both match up the variable minsPassed will have incremented the total number of
        # minutes between the two times.
        while (futureHr != nowHr) | (futureMin != nowMin):
            nowMin += 1
            minsPassed += 1
            if nowMin == 60:
                nowHr += 1
                hrsPassed += 1
                if nowHr == 24:
                    nowHr = 0
                nowMin = 0

        # convert minsPassed to seconds to pass to time.sleep()
        sleepTime = minsPassed * 60
        time.sleep(sleepTime)
        open_file(app.getEntry('alarmsound'))

    # The snooze button. Self explanitory.
    elif btn == 'Snooze':
        time.sleep(600)
        open_file(app.getEntry('alarmsound'))


# gui definitions. The code is roughly organized in the same way it appears on the gui window
app = gui()
app.setFont(20)
app.setBg('Pink')

app.startLabelFrame("Let me sleep!  (╯°□°）╯︵ ┻━┻)")
app.addLabel("info", "How long do you want to nap?", 1, 0)

app.addLabel('hrs', 'Hours', 2, 1)
app.addEntry('hrs', 2, 0)


app.addLabel('min', 'Minutes', 3, 1)
app.addEntry('min', 3, 0)


app.addLabel('sec', 'Seconds', 4, 1)
app.addEntry('sec', 4, 0)


app.addOptionBox('alarmtype', ['Local Song', 'YT URL'], 5, 1)
app.addEntry('alarmsound', 5, 0)


app.addButtons(['Nap this long', 'Snooze'], press, 6, 0, 0)

app.addHorizontalSeparator(7, 0, 4, colour="black")

app.addButtons(['Nap until'], press, 8, 0, 0)

app.addOptionBox('Time', [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], 9, 0, 1)
app.addOptionBox('mintime', range(0, 60), 9, 1, 0)
app.addOptionBox('ampm', ['AM', 'PM'], 9, 2, 0)

app.setOptionBoxPadding('Time', [150, 0])
app.setOptionBoxPadding('mintime', [20, 0])

app.stopLabelFrame()
app.go()
