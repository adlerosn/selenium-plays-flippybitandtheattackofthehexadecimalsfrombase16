#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

from pathlib import Path

from selenium import webdriver

URL = 'https://flippybitandtheattackofthehexadecimalsfrombase16.com/'
JS = Path('play-v2.user.js').read_text(encoding='utf-8', errors='strict')


def main():
    driver = webdriver.Firefox()
    try:
        driver.get(URL)
        driver.execute_script(JS)
        game = driver.find_element_by_css_selector("body")
        while True:
            keys = driver.execute_script("return get_keys_to_press().join('')")
            game.send_keys(keys)
    finally:
        driver.close()


if __name__ == '__main__':
    main()
