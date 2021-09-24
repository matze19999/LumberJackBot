from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from PIL import ImageGrab, Image
from mss import mss
import time

#Highscore: 1004

# https://yangcha.github.io/iview/iview.html

url = 'https://tbot.xyz/lumber/#ey'

# Set Pixels here
# 3440 x 1440
x_left = 800
x_right = 922
abstand = 50
y_begin = 970
anzahl_aeste = 6
y_end = y_begin - (anzahl_aeste * abstand)

# 1920 x 1080
x_left = 430
x_right = 536
abstand = 100
y_begin = 609
anzahl_aeste = 5
y_end = y_begin - (anzahl_aeste * abstand)

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

with mss() as sct:

    while True:
        next_moves = []
        color_left = []
        color_right = []
        sct_img = sct.grab(sct.monitors[1])
        img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
        px = img.load()

        for i in range(y_begin, y_end, -abstand ):
            color_left.append(str(px[x_left, i]))
            color_right.append(str(px[x_right, i]))

        for i in range(0, anzahl_aeste, 1):
            if '161' in str(color_left[i]):
                print('R')
                next_moves.append('R')
                next_moves.append('R')
            elif '161' in str(color_right[i]):
                print('L')
                next_moves.append('L')
                next_moves.append('L')

        #print(next_moves)
        for move in next_moves:
            if move == 'L':
                browser.find_element_by_class_name('_hover').send_keys(Keys.ARROW_LEFT)
            else:
                browser.find_element_by_class_name('_hover').send_keys(Keys.ARROW_RIGHT)

        time.sleep(0.05)
