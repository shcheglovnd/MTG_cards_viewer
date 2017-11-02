from django.http import HttpResponse
from django.template import loader

from .models import Card


def index(request):
    all_cards_list = Card.objects.all()
    template = loader.get_template('cards/index.html')
    context = {
        'all_cards_list': all_cards_list,
    }
    return HttpResponse(template.render(context, request))


def search(request):
    name = request.GET.get('name')
    found_card = Card.objects.filter(card_name=name).first()
    template = loader.get_template('cards/search.html')
    context = {
        'card': found_card,
    }
    return HttpResponse(template.render(context, request))
