import requests
import urllib3
from bs4 import BeautifulSoup
from tools.card_images_downloader import download_file
from django.http import HttpResponse
from django.template import loader

from .models import Card

MAGIC_CARDS_SITE_URL = 'https://magiccards.info'


def index(request):
    template = loader.get_template('cards/search_block.html')
    context = {
        'user': 'user',
    }
    return HttpResponse(template.render(context, request))


def list_all(request):
    all_cards_list = Card.objects.all()
    template = loader.get_template('cards/list.html')
    context = {
        'all_cards_list': all_cards_list,
    }
    return HttpResponse(template.render(context, request))


def search(request):
    result_card_name = ''
    result_card_local_path = ''
    is_card_found = False

    searching_name = request.GET.get('name')
    card_from_local_db = Card.objects.filter(name=searching_name).first()

    if card_from_local_db:
        result_card_name = card_from_local_db.name
        result_card_local_path = card_from_local_db.local_path
        is_card_found = True
    else:
        card_from_site = search_on_magic_cards_site(searching_name)
        if card_from_site:
            result_card_name = card_from_site['name']
            result_card_local_path = card_from_site['local_path']
            is_card_found = True

            if not is_card_in_local_db(result_card_name):
                card_image_url = MAGIC_CARDS_SITE_URL + result_card_local_path
                try:
                    download_file(card_image_url)
                except urllib3.exceptions.MaxRetryError:
                    print('Cant download card image')
                else:
                    save_card_to_local_db(result_card_name, result_card_local_path)

    template = loader.get_template('cards/result.html')
    context = {
        'card': {'name': result_card_name, 'local_path': 'cards/images' + result_card_local_path},
        'searching_name': searching_name,
        'is_card_found': is_card_found
    }
    return HttpResponse(template.render(context, request))


def search_on_magic_cards_site(name):
    response = requests.get('{}/query?q=!{}'.format(MAGIC_CARDS_SITE_URL, name))
    soup = BeautifulSoup(response.text, 'html.parser')
    card = soup.find(lambda tag: tag.name == 'img' and name.lower() in tag['alt'].lower())
    if card:
        return {'name': card['alt'], 'local_path': card['src']}


def is_card_in_local_db(name):
    if Card.objects.filter(name=name).first():
        return True
    else:
        return False


def save_card_to_local_db(name, local_path):
    new_card = Card(
        name=name,
        local_path=local_path
    )
    new_card.save()


