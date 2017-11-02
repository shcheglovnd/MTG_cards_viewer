import django
import json
import os
import sys

sys.path.insert(0, os.path.abspath('../mtgcards_service'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mtgcards_service.settings')
django.setup()

from cards.models import Card


def push():
    print(os.getcwd())
    print(Card.objects.all())
    with open('../tools/cards.json', 'r') as f:
        cards = json.load(f)
    counter = 0
    for c in cards:
        counter += 1
        if counter > 10:
            break
        card_name = c['card_name']
        path = c['card_image_url'].split('info')[1]
        card = Card(card_name=card_name, path=path)
        card.save()


if __name__ == '__main__':
    push()
