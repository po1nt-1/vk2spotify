import json
import time
from random import randint

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options


def load_config():
    global CONFIG
    with open('config.json', 'r') as f:
        CONFIG = json.load(f)


def vk():
    opts = Options()
    opts.add_argument('--headless')
    with webdriver.Firefox(executable_path='./geckodriver',
                           options=opts) as driver:
        driver.get(f'https://m.vk.com/audios{CONFIG.get("vk_audio_url")}')
        input_elems = driver.find_elements_by_tag_name('input')
        input_elems[0].clear()
        input_elems[0].send_keys(CONFIG.get('vk_login'))
        input_elems[1].clear()
        input_elems[1].send_keys(CONFIG.get('vk_password'))
        input_elems[1].send_keys(Keys.RETURN)
        time.sleep(5)

        last_height = 0
        last_time = 0
        while True:
            sleep_time = randint(6, 10) / 10
            new_height = driver.execute_script("""
                window.scrollBy(0, -100);
                window.scrollTo(0, document.body.scrollHeight);
                return document.body.scrollHeight;
            """)
            if new_height == last_height:
                if time.time() - last_time < sleep_time + 0.1:
                    break
                last_time = time.time()
            last_height = new_height
            print('.', end='')
            time.sleep(sleep_time)

        raw = driver.find_elements_by_css_selector(
            "div[class^='audio_item audio_item_")

        audio_list = []
        id = 0
        for elem in raw:
            audio_list.append({
                'id': id,
                'artist': f'{elem.text.splitlines()[1]}',
                'title': f'{elem.text.splitlines()[0]}'
            })
            id += 1

        with open('data.json', 'w') as f:
            json.dump(audio_list, f, ensure_ascii=False, indent=4)


def spotify():
    pass


def main():
    load_config()
    vk()
    spotify()


if __name__ == '__main__':
    main()
