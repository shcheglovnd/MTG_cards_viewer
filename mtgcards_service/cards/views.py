from django.http import HttpResponse
from django.template import loader

from .models import Card


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
    name = request.GET.get('name')
    found_card = Card.objects.filter(name=name).first()
    template = loader.get_template('cards/result.html')
    if found_card:
        found_card.local_path = 'cards/images' + found_card.local_path
    context = {
        'card': found_card,
    }
    return HttpResponse(template.render(context, request))


