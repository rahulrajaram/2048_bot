"""
Script automatically plays the 2048 game at https://play2048.co a 100 times

Prerequisites:

    1. Python 3.6+

    2. `selenium` Python package from PyPi:

        pip install selenium

    3. Firefox Web Browser

    4. geckodriver (on Arch, you can get it by running:

        pacman -S geckodriver
"""
import time
import datetime
import random

from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys


BROWSER = webdriver.Firefox()
BROWSER.get('https://play2048.co')
GAME_CONTAINER = BROWSER.find_elements_by_class_name('game-container')[0]
MAX_SCORE = 0
ACTIONS = [
    Keys.ARROW_UP,
    Keys.ARROW_DOWN,
    Keys.ARROW_LEFT,
    Keys.ARROW_RIGHT,
]


def restart_game():
    """
    Function finds the 'New Game' button and clicks it
    """
    restart_button = BROWSER.find_elements_by_class_name('restart-button')[0]
    restart_button.click()


def update_max_score(i):
    """
    Function retrieves the latest local score and updates MAX_SCORE when exceeded
    """
    global MAX_SCORE
    score_container = BROWSER.find_elements_by_class_name('score-container')[0]
    # Exclude spurious characters that occupy the score-container
    local_score = int(score_container.text.split('\n')[0])
    if local_score > MAX_SCORE:
        MAX_SCORE = local_score
    print(f'{i}. Score: {local_score}')


def play_once(i):
    """
    Function repeats random directional key strokes until it is no longer
    possible to make a move
    """
    while True:
        ActionChains(BROWSER).key_down(
            random.sample(ACTIONS, k=1)[0]
        ).perform()
        try:
            time.sleep(0.01)
            _ = BROWSER.find_elements_by_class_name('game-over')[0]
            update_max_score(i)
            break
        except IndexError:
            pass


def main():
    """
    Function plays the 2048 game a 100 times before cleaning up Firefox
    """
    for i in range(1, 101):
        play_once(i)
        restart_game()
    BROWSER.stop_client()
    BROWSER.quit()
    print(f'Highest score: {MAX_SCORE}')


if __name__ == '__main__':
    main()
