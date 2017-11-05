import json
import os
import requests
import sys
from concurrent.futures import ThreadPoolExecutor

DEFAULT_FILE_PATH = 'cards.json'

counter = 0
files_count = 0


def get_cards_urls_from_json(input_json_file):
    urls = []
    with open(input_json_file, 'r') as f:
        cards = json.load(f)
    for card in cards:
        urls.append(card['card_image_url'])
    global files_count
    files_count = len(cards)
    return urls


def download_static_image_file(url):
    image_path = url.split('info')[1]
    local_path = 'cards/static/cards/images' + image_path
    os.makedirs(os.path.dirname(local_path), exist_ok=True)
    r = requests.get(url, stream=True)
    with open(local_path, 'wb') as f:
        for chunk in r:
            f.write(chunk)

    global counter
    counter += 1
    print('{}/{} file {} downloaded'.format(counter, files_count, image_path))


def check_downloaded_images(urls):
    for url in urls:
        image_path = url.split('info')[1]
        local_path = 'images' + image_path
        if not os.path.isfile(local_path):
            print('File {} not exists'.format(image_path))
    print('Checking ends')


def download_cards_images(images_data):
    urls = get_cards_urls_from_json(images_data)
    print(len(urls))
    executor = ThreadPoolExecutor(max_workers=10)
    executor.map(download_static_image_file, urls)
    check_downloaded_images(urls)


if __name__ == '__main__':
    if len(sys.argv) == 1:
        download_cards_images(DEFAULT_FILE_PATH)
    elif len(sys.argv) == 2:
        download_cards_images(sys.argv[1])
    else:
        sys.exit('You need to specify only file path as first argument')
