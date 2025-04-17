"""
Script automatically plays the 2048 game at https://play2048.co

Prerequisites:

    1. Python 3.6+

    2. `selenium` Python package from PyPi:

        pip install selenium

    3. Firefox Web Browser

    4. geckodriver (on Arch, you can get it by running:

        pacman -S geckodriver
"""

import copy
import time
import datetime
import random

from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

import game

print("Starting 2048 bot...")
BROWSER = webdriver.Firefox()
BROWSER.get("https://play2048.co")

# Wait for the page to load and the game to be ready
print("Waiting for page to load completely...")
time.sleep(3)  # Give the page some time to load

# The website structure has changed, so we'll interact directly with the keyboard
print("Page loaded, starting game...")
MAX_SCORE = 0


def update_max_score(i):
    """
    Function retrieves the latest local score and updates MAX_SCORE when exceeded
    """
    global MAX_SCORE
    try:
        # Try to find the score element with the new structure
        score_elements = BROWSER.find_elements(By.CLASS_NAME, "text-tan")
        if score_elements:
            for element in score_elements:
                try:
                    # Extract the score from the element text
                    text = element.text
                    if "SCORE" in text.upper():
                        # Extract the number from the text
                        score_text = "".join(c for c in text if c.isdigit())
                        if score_text:
                            local_score = int(score_text)
                            if local_score > MAX_SCORE:
                                MAX_SCORE = local_score
                            print(f"{i}. Score: {local_score}")
                            return
                except Exception as e:
                    print(f"Error parsing score: {e}")

        print(f"{i}. Could not find score")
    except Exception as e:
        print(f"Error updating score: {e}")


def is_game_over():
    """
    Check if the game is over by looking for game-over related elements
    or by checking if no moves are possible
    """
    try:
        # Look for any indication that the game is over
        body = BROWSER.find_element(By.TAG_NAME, "body")
        return "game-over" in body.get_attribute("class")
    except:
        # If we can't determine, assume it's not over
        return False


def play_once(i):
    """
    Function repeats directional key strokes until it is no longer
    possible to make a move
    """
    # Focus on the body to ensure key presses are captured
    body = BROWSER.find_element(By.TAG_NAME, "body")
    body.click()

    # Play the game with random moves
    moves = 0
    while moves < 1000:  # Limit to prevent infinite loops
        # Choose a random direction
        direction = random.choice(
            [Keys.ARROW_UP, Keys.ARROW_DOWN, Keys.ARROW_LEFT, Keys.ARROW_RIGHT]
        )

        # Send the key press
        ActionChains(BROWSER).key_down(direction).key_up(direction).perform()

        # Small delay to let the game process the move
        time.sleep(0.1)

        # Check if game is over
        if is_game_over():
            update_max_score(i)
            break

        moves += 1

        # Update score every 10 moves
        if moves % 10 == 0:
            update_max_score(i)


def main():
    try:
        play_once(1)
    finally:
        # Always clean up
        print(f"Highest score: {MAX_SCORE}")
        BROWSER.quit()


if __name__ == "__main__":
    main()
