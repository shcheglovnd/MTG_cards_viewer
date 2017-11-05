import django
import json
import os
import sys

sys.path.insert(0, os.path.abspath('../'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mtgcards_service.settings')
django.setup()
from cards.models import Card

DEFAULT_FILE_PATH = 'cards.json'


def push_from_json(json_file_path):
    with open(json_file_path, 'r') as f:
        cards = json.load(f)
    counter = 0
    size = len(cards)
    for card in cards:
        new_card = Card(
            name=card['card_name'],
            local_path=card['card_image_url'].split('info')[1]
        )
        new_card.save()
        counter += 1
        print('{}/{} card pushed'.format(counter, size))


if __name__ == '__main__':
    if len(sys.argv) == 1:
        push_from_json(DEFAULT_FILE_PATH)
    elif len(sys.argv) == 2:
        push_from_json(sys.argv[1])
    else:
        sys.exit('You need to specify only file path as first argument')
