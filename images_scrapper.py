import requests
from bs4 import BeautifulSoup

SITEMAP_URL = 'https://magiccards.info/sitemap.html'
EDITION = 'https://magiccards.info/akh/en.html'


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


def main():
    print(collect_edition_cards_numbers(EDITION))


main()


