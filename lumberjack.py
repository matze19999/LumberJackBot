while True:
    try:
        import os
        from selenium import webdriver
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.webdriver.common.action_chains import ActionChains
        from selenium.webdriver.common.keys import Keys
        from PIL import Image
        from mss import mss
        import mss
        import time
        import win32com.client as comctl
        break
    except ModuleNotFoundError:
        os.system("pip3 install --upgrade selenium mss pywin32 pillow")


wsh = comctl.Dispatch("WScript.Shell")

#Highscore: 1004

# Check coordiantes of screenshot here
# https://yangcha.github.io/iview/iview.html

url = 'https://tbot.xyz/lumber/#ey'

# Set Pixels here
# 3440 x 1440
x_left = 10 # linker Balken
x_right = 80 # rechter Balken
y_begin = 577 # Beginn erster Ast
abstand = 100 # Abstand zwischen Ästen
anzahl_aeste = 5 # Wie viel Äste vorberechnet werden sollen
y_end = y_begin - ((anzahl_aeste + 1) * abstand)
monitor = {"top": 390, "left": 820, "width": 90, "height": 700} # Bildausschnitt des Monitors für Screenshots

'''# 1920 x 1080
x_left = 430  # linker Balken
x_right = 536  # rechter Balken
abstand = 100 # abstand zwischen Ästen
y_begin = 609 # Beginn erster Ast
anzahl_aeste = 4 # Wie viel Äste vorberechnet werden sollen
y_end = y_begin - ((anzahl_aeste + 1) * abstand)
monitor = {"top": 390, "left": 820, "width": 90, "height": 700}'''

# Initialisiere Browser
options = webdriver.ChromeOptions()
options.add_argument('window-size=1200x600')
options.add_argument('disable-features=InfiniteSessionRestore')
options.add_argument("--disable-dev-shm-usage")
options.add_experimental_option("w3c", False)
options.add_experimental_option('excludeSwitches', ['enable-logging'])

browser = webdriver.Chrome(options=options)
actions = ActionChains(browser)

browser.get(url)

browser.find_element_by_css_selector('#details-button').click()

browser.find_element_by_css_selector('#proceed-link').click()
time.sleep(1)
browser.find_element_by_class_name('_hover').send_keys(Keys.SPACE)
time.sleep(0.7)

with mss.mss() as sct:
    sct_img = sct.grab(monitor)
    #mss.tools.to_png(sct_img.rgb, sct_img.size, output=output) Save Screenshot to current folder
    img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
    px = img.load()
    color_right_1 = str(px[x_right, y_begin])
    if '161' in color_right_1:
        wsh.SendKeys("{LEFT}")
        wsh.SendKeys("{LEFT}")
    else:
        wsh.SendKeys("{RIGHT}")
        wsh.SendKeys("{RIGHT}")

    while True:
        next_moves = []
        color_left = []
        color_right = []
        sct_img = sct.grab(monitor)
        img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
        px = img.load()

        for i in range(y_begin, y_end, -abstand ):
            if '161' in str(px[x_left, i]):
                next_moves.append('R')
                next_moves.append('R')
            elif '161' in str(px[x_right, i]):
                next_moves.append('L')
                next_moves.append('L')

        print(next_moves)
        for move in next_moves:
            if move == 'L':
                wsh.SendKeys("{LEFT}")
                time.sleep(0.0001)
            else:
                wsh.SendKeys("{RIGHT}")
                time.sleep(0.0001)
        time.sleep(0.05)
