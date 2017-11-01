import json
import os
import requests
from concurrent.futures import ThreadPoolExecutor

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


def download_file(url):
    image_path = url.split('info')[1]
    local_path = 'images' + image_path
    os.makedirs(os.path.dirname(local_path), exist_ok=True)
    r = requests.get(url, stream=True)
    with open(local_path, 'wb') as f:
        for chunk in r:
            f.write(chunk)

    global counter
    counter += 1
    print('{}/{} file {} downloaded'.format(counter, files_count, image_path))


def download_cards_images():
    urls = get_cards_urls_from_json('cards.json')
    executor = ThreadPoolExecutor(max_workers=10)
    executor.map(download_file, urls)


def main():
    download_cards_images()


if __name__ == '__main__':
    main()
