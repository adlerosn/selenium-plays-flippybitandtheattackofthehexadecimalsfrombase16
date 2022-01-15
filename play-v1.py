#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

import random
from time import sleep
from typing import List

from selenium import webdriver

URL = 'https://flippybitandtheattackofthehexadecimalsfrombase16.com/'


def main():
    driver = webdriver.Firefox()
    driver.get(URL)
    driver.execute_script(
        "!function(){var tdtoremove = document.querySelector('td');tdtoremove.parentNode.removeChild(tdtoremove);delete tdtoremove;}();"
    )
    while driver.execute_script(
            "return document.querySelector('#game-container') === null;"
    ):
        sleep(0.1)
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
        new_data = driver.execute_script(
            "return [...document.querySelectorAll('.enemy:not(.under-attack)')].map(x=>x.innerText.trim()).join(',');"
        )
        new_data = list(
            map(lambda a: int(a, 16), filter(len, new_data.split(','))))
        current_data = new_data[:]
        if (datalen := len(current_data)) > 0:
            print(f'Still on screen: {len(new_data)}')
            print(f'New enemies: {bytearray(current_data).hex().upper()}')
            for enemy_number in current_data:
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
                game.send_keys(''.join(keypresses))
                sleep(0.1/(datalen**2))
        else:
            sleep(0.1)


if __name__ == '__main__':
    main()
