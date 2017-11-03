import requests
import urllib3
from bs4 import BeautifulSoup
from tools.card_images_downloader import download_file
from django.http import HttpResponse
from django.template import loader

from .models import Card

MAGIC_CARDS_SITE = 'https://magiccards.info'


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
    card_name = ''
    card_local_path = 'cards/images'
    is_card_found = False
    name = request.GET.get('name')
    card_from_db = Card.objects.filter(name=name).first()
    if card_from_db:
        card_name = card_from_db.name
        card_local_path += card_from_db.local_path
        is_card_found = True
    else:
        response = requests.get('{}/query?q=!{}'.format(MAGIC_CARDS_SITE, name))
        soup = BeautifulSoup(response.text, 'html.parser')
        card = soup.find(lambda tag: tag.name == 'img' and name.lower() in tag['alt'].lower())

        if card:
            card_name = card['alt']
            card_local_path += card['src']
            is_card_found = True

            if not Card.objects.filter(name=card['alt']).first():
                img_url = MAGIC_CARDS_SITE + card['src']
                try:
                    download_file(img_url)
                except urllib3.exceptions.MaxRetryError:
                    print('cant load image')
                else:
                    new_card = Card(
                        name=card['alt'],
                        local_path=card['src']
                    )
                    new_card.save()

    template = loader.get_template('cards/result.html')
    context = {
        'card': {'name': card_name, 'local_path': card_local_path},
        'searching_name': name,
        'is_card_found': is_card_found
    }
    return HttpResponse(template.render(context, request))


