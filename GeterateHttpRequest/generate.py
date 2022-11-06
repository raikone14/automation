import webbrowser
import os
import time


while True:


    webbrowser.open('http://google.com')
    time.sleep(5)
    os.system("taskkill /im firefox.exe /f")
