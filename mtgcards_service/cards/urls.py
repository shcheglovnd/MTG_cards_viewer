from django.conf.urls import url

from . import views

app_name = 'cards'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^search$', views.search, name='search'),
]
