#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

import random
from time import sleep
from typing import List

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

URL = 'https://flippybitandtheattackofthehexadecimalsfrombase16.com/'


def main():
    driver = webdriver.Firefox()
    driver.get(URL)
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
    game.send_keys("1")
    previous_data: List[str] = list()
    while True:
        new_data = driver.execute_script(
            "return [...document.querySelectorAll('.enemy')].map(x=>x.innerText.trim());"
        )
        current_data = new_data[:]
        for previous_datapoint in previous_data:
            if previous_datapoint in current_data:
                current_data.pop(current_data.index(previous_datapoint))
        if (datalen := len(current_data)) > 0:
            print(f'New enemies: {current_data}')
            for enemy_number in current_data:
                keys = ('0'*8+bin(int(enemy_number, 16))[2:])[-8:]
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
        previous_data = new_data

    # driver.close()


if __name__ == '__main__':
    main()
