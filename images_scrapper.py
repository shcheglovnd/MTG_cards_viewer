import requests
from bs4 import BeautifulSoup

MAIN_URL = 'https://magiccards.info/'
SITEMAP_URL = 'https://magiccards.info/sitemap.html'
EDITION_TPL = 'https://magiccards.info/{}/en.html'
CARD_TPL = 'https://magiccards.info/{}/en/{}.html'


# TODO lists to tuples?

def collect_all_editions(sitemap_url):
    editions_list = []
    response = requests.get(sitemap_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    small_tags_list = soup.find_all('table')[1].find_all('small')
    for t in small_tags_list:
        editions_list.append(t.text)
    return editions_list


def collect_edition_cards_numbers(edition_url):
    cards_numbers_list = []
    response = requests.get(edition_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    table_rows_list = soup.find_all('table')[3].find_all('tr')
    table_rows_list.pop(0)
    for r in table_rows_list:
        card_number = r.find('td').text
        cards_numbers_list.append(card_number)
    return cards_numbers_list


def cards_numbers_to_editions():
    result = {}
    editions = collect_all_editions(SITEMAP_URL)
    for e in editions:
        edition_url = EDITION_TPL.format(e)
        edition_cards = collect_edition_cards_numbers(edition_url)
        result.update({e: edition_cards})
        # break # delete this after tests
        print('{} edition complete'.format(e))
    return result


def main():
    print(cards_numbers_to_editions())


main()


