#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

import random
import threading
from pathlib import Path
from time import sleep

from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement

URL = 'https://flippybitandtheattackofthehexadecimalsfrombase16.com/'


def main():
    driver = webdriver.Firefox()
    driver.set_window_size(525, 900)
    try:
        threading.Thread(target=lambda: driver.get(URL)).start()
        sleep(0.25)
        while driver.execute_script(
                "return document.querySelector('#game-container') === null;"
        ):
            sleep(0.1)
        driver.execute_script(
            "!function(){var tdtoremove = document.querySelector('td');tdtoremove.parentNode.removeChild(tdtoremove);delete tdtoremove;}();"
        )
        game = driver.find_element_by_css_selector("body")
        game.send_keys(".")  # unmute tab
        sleep(0.1)
        while driver.execute_script(
                "return document.querySelector('#logo')?.style?.display !== 'block';"
        ):
            sleep(0.1)
        sleep(1.5)
        game.send_keys("1")
        while True:
            data = driver.execute_script(
                "return [...document.querySelectorAll('.enemy:not(.under-attack)')].map(x=>x.innerText.trim()).join(',');"
            )
            data = list(map(lambda a: int(a, 16),
                        filter(len, data.split(','))))
            if (datalen := len(data)) > 0:
                print(f'Still on screen: {len(data)}')
                print(f'New enemies: {bytearray(data).hex().upper()}')
                for enemy_number in data:
                    keys = ('0'*8+bin(enemy_number)[2:])[-8:]
                    keypresses = list(map(
                        lambda x: x[0],
                        filter(
                            lambda x: x[1] == '1',
                            map(
                                lambda x: (f'{x[0]+1}', x[1]),
                                enumerate(keys)
                            ))))
                    random.shuffle(keypresses)
                    game.send_keys(''.join(keypresses)+' ')
                    sleep(0.1/(datalen**2))
            else:
                sleep(0.1)
                screenshot_and_restart_on_game_over(driver, game)

    finally:
        driver.close()


def screenshot_and_restart_on_game_over(driver: webdriver.Firefox, game: WebElement):
    if(driver.execute_script(
        "return document.querySelector('html.game-over') !== null;"
    )):
        sleep(3)
        if(driver.execute_script(
            "return document.querySelector('html.game-over') !== null;"
        )):
            Path('scores').mkdir(exist_ok=True, parents=True)
            score = driver.execute_script(
                "return parseInt(document.querySelector('#score').innerText.trim());"
            )
            hiscore_path = Path('hiscore.txt')
            if not hiscore_path.exists():
                hiscore_path.write_text(str(-1), encoding='utf-8')
            hiscore = int(
                hiscore_path.read_text('utf-8').strip())
            if score > hiscore:
                score_path = Path('score/screenshot_%04d.png' %
                                  score).absolute()
                game.screenshot(str(score_path))
                if not score_path.is_file():
                    raise FileNotFoundError(score_path)
                hiscore_path.write_text(str(score))
            sleep(.2)
            game.send_keys('1 1 ')


if __name__ == '__main__':
    main()
