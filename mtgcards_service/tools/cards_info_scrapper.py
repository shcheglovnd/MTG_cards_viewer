import json
import requests
import sys
from bs4 import BeautifulSoup

SITEMAP_URL = 'https://magiccards.info/sitemap.html'
EDITION_URL_TPL = 'https://magiccards.info/{}/en.html'
CARD_IMG_URL_TPL = 'https://magiccards.info/scans/en/{}/{}.jpg'
DEFAULT_FILE_PATH = 'cards.json'

def collect_all_editions():
    editions_list = []
    response = requests.get(SITEMAP_URL)
    soup = BeautifulSoup(response.text, 'html.parser')
    small_tags_list = soup.find_all('table')[1].find_all('small')
    for t in small_tags_list:
        editions_list.append(t.text)
    return editions_list


def collect_edition_cards_info(edition):
    edition_cards = []
    edition_url = EDITION_URL_TPL.format(edition)
    response = requests.get(edition_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    table_rows_list = soup.find('table', cellpadding='3').find_all('tr')
    table_rows_list.pop(0)
    for r in table_rows_list:
        card_number = r.find('td').text
        card_name = r.find_all('td')[1].find('a').text
        edition_cards.append({'card_name': card_name, 'card_number': card_number, 'edition': edition})
    return edition_cards


def cards_numbers_to_editions():
    cards = []
    editions = collect_all_editions()
    for e in editions:
        edition_cards = collect_edition_cards_info(e)
        cards.extend(edition_cards)
        print('{} edition complete'.format(e))
    return cards


def get_cards_list():
    cards = cards_numbers_to_editions()
    for card in cards:
        card_image_url = CARD_IMG_URL_TPL.format(card['edition'], card['card_number'])
        card.update({'card_image_url': card_image_url})
    return cards


def cards_to_json_file(file_path):
    cards_list = get_cards_list()
    with open(file_path, 'w') as f:
        f.write(json.dumps(cards_list, sort_keys=True, indent=4))
    print('Urls exported to file')


if __name__ == '__main__':
    if len(sys.argv) == 1:
        cards_to_json_file(DEFAULT_FILE_PATH)
    elif len(sys.argv) == 2:
        cards_to_json_file(sys.argv[1])
    else:
        sys.exit('You need to specify only file path as first argument')



