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
    size = len(cards)
    for card in cards:
        new_card = Card(
            name=card['card_name'],
            local_path=card['card_image_url'].split('info')[1],
            original_path=card['card_image_url'],
            edition=card['edition'],
            number_in_edition=card['card_number']
        )
        new_card.save()
        counter += 1
        print('{}/{} card pushed'.format(counter, size))


if __name__ == '__main__':
    push()
