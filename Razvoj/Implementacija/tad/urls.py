from django.urls import path

from .views import *

urlpatterns = [
    path('', index,name='index'),
    path('RegKor', regkor,name='regkor'),
    path('KorisnikPocetna', korpoc,name='korpoc'),
    path('KorisnikPregled', korpregled,name='korpregled'),
    path('insert_oglas/', insert_oglas, name='insert_oglas'),
    path('out/', out, name='out'),
    path('create_oglas', create_oglas, name = 'create_oglas'),
    path('OrganizatorPocetna', orgpoc, name = 'orgpoc'),
    path('pravljenjeOglasa', orgPravljenjeOglasa, name = 'pravljenjeOglasa')
]