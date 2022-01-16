#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

import random
from pathlib import Path
from time import sleep
from typing import List

from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement

URL = 'https://flippybitandtheattackofthehexadecimalsfrombase16.com/'
BUFFER_SIZE = 64
BUFFER_PREPARE_SIZE = 1024
DISABLE_ANIMATIONS = True


def main():
    driver = webdriver.Firefox()
    driver.set_window_size(525, 900)
    try:
        driver.get(URL)
        sleep(0.25)
        while driver.execute_script(
                "return document.querySelector('#game-container') === null;"
        ):
            sleep(0.1)
        driver.execute_script(
            "!function(){var tdtoremove = document.querySelector('td');tdtoremove.parentNode.removeChild(tdtoremove);delete tdtoremove;}();"
        )
        if DISABLE_ANIMATIONS:
            driver.execute_script(
                """!function(){
                    document.body.parentNode.classList.add('novibrate');
                    var s = document.createElement('style');
                    var st = 'html { transform: none !important; } ';
                    st += '.missile.hover { animation-name: none !important; } ';
                    st += '.missile { transition-property: none !important; } ';
                    st += '.firing { left: 0px !important; bottom: 0px !important; display: none !important; } ';
                    st += '.explosion { left: 0px !important; bottom: 0px !important; display: none !important; } ';
                    st += '.enemy.under-attack { filter: hue-rotate(120deg); } ';
                    s.innerText = st;
                    document.head.appendChild(s);
                }();"""
            )
        game = driver.find_element_by_css_selector("body")
        game.send_keys(".")  # unmute tab
        sleep(0.1)
        while driver.execute_script(
                "return document.querySelector('#logo')?.style?.display !== 'block';"
        ):
            sleep(0.1)
        sleep(1.5)
        screenshot_statup(driver, game)
        game.send_keys("1 ")
        while True:
            main_cycle(driver, game)
    finally:
        driver.quit()


def main_cycle(driver: webdriver.Firefox, game: WebElement):
    data = driver.execute_script(
        "return [...document.querySelectorAll('.enemy:not(.under-attack)')].map(x=>x.innerText.trim()).join(',');"
    )
    data = list(map(lambda a: int(a, 16),
                filter(len, data.split(','))))
    if (datalen := len(data)) > 0:
        print(f'New enemies: [{datalen}]{bytearray(data).hex().upper()}')
        tosleep = 0.0
        if datalen < BUFFER_SIZE:
            tosleep = 0.1/(datalen**2)
        deferred_keys = sort_keystrokes(
            list(map(enemy_number_to_keys, data))[:BUFFER_PREPARE_SIZE])
        for ks in deferred_keys[:BUFFER_SIZE]:
            game.send_keys(ks+' ')
            sleep(tosleep)
    else:
        sleep(0.1)
        screenshot_and_restart_on_game_over(driver, game)


def shuffled(a):
    b = list(a)
    random.shuffle(b)
    return b


def sort_keystrokes(keystrokes: List[str]) -> List[str]:
    return list(map(lambda a: ''.join(shuffled(a)), keystrokes))


def enemy_number_to_keys(enemy_number: int) -> str:
    keys = ('0'*8+bin(enemy_number)[2:])[-8:]
    keypresses = list(map(
        lambda x: x[0],
        filter(
            lambda x: x[1] == '1',
            map(
                lambda x: (f'{x[0]+1}', x[1]),
                enumerate(keys)
            ))))
    return ''.join(keypresses)


def screenshot_statup(driver: webdriver.Firefox, game: WebElement):
    Path('scores').mkdir(exist_ok=True, parents=True)
    score_path = Path('scores/startup.png')
    driver.get_screenshot_as_file(str(score_path))
    if not score_path.is_file():
        raise FileNotFoundError(score_path)


def screenshot_and_restart_on_game_over(driver: webdriver.Firefox, game: WebElement):
    if(driver.execute_script(
        "return document.querySelector('html.game-over') !== null;"
    )):
        score = driver.execute_script(
            "return parseInt(document.querySelector('#score').innerText.trim());"
        )
        print(f'{score=}')
        sleep(3)
        if(driver.execute_script(
            "return document.querySelector('html.game-over') !== null;"
        )):

            Path('scores').mkdir(exist_ok=True, parents=True)
            score = driver.execute_script(
                "return parseInt(document.querySelector('#score').innerText.trim());"
            )
            print(f'{score=}')
            print('\n'*3)
            hiscore_path = Path('hiscore.txt')
            if not hiscore_path.exists():
                hiscore_path.write_text(str(-1), encoding='utf-8')
            hiscore = int(
                hiscore_path.read_text('utf-8').strip())
            if score > hiscore:
                score_path = Path('scores/screenshot_%04d.png' %
                                  score).absolute()
                game.screenshot(str(score_path))
                if not score_path.is_file():
                    raise FileNotFoundError(score_path)
                hiscore_path.write_text(str(score))
            sleep(.2)
            game.send_keys('1 1 ')


if __name__ == '__main__':
    main()
