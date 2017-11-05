import requests
import urllib3
from bs4 import BeautifulSoup
from tools.card_images_downloader import download_file
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .models import Card
from .models import Purchases

MAGIC_CARDS_SITE_URL = 'https://magiccards.info'
SEARCH_PRICE = 50


def index(request):
    template = loader.get_template('cards/search_block.html')
    context = {
        'user': 'user',
    }
    return HttpResponse(template.render(context, request))


@login_required(login_url='/login/')
def search(request):
    result_card_name = ''
    result_card_local_path = ''
    is_card_found = False

    is_money_enough = request.user.profile.money >= SEARCH_PRICE
    searching_name = request.GET.get('name')

    if is_money_enough or is_user_made_this_query(searching_name):
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
        if not is_user_made_this_query(searching_name):
            save_user_query(searching_name, request.user)
            dec_user_money(request.user.id, SEARCH_PRICE)
            request.user.profile.money -= SEARCH_PRICE

    template = loader.get_template('cards/result.html')
    context = {
        'card': {'name': result_card_name, 'local_path': 'cards/images' + result_card_local_path},
        'searching_name': searching_name,
        'is_card_found': is_card_found,
        'is_money_enough': is_money_enough,
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


def dec_user_money(user_id, count):
    user = User.objects.get(id=user_id)
    user.profile.money -= count
    user.save()


def is_user_made_this_query(query):
    purchase = Purchases.objects.filter(query=query).first()
    if purchase:
        return True
    else:
        return False


def save_user_query(query, user):
    purchase = Purchases(query=query, user=user)
    purchase.save()


