from django.urls import path

from .views import *

urlpatterns = [

    path('', index,name='index'),
    path('Admin', adminpoc, name = 'adminpoc'),
    path('UkloniKor', uklonikor, name = 'uklonikor'),
    path('prihvati', prihvati, name = 'prihvati'),
    path('odbij', odbij, name = 'odbij'),
    path('RegKor', regkor,name='regkor'),
    path('RegOrg', regorg,name='regorg'),
    path('KorisnikPocetna', korpoc,name='korpoc'),
    path('KorisnikPregled', korpregled,name='korpregled'),
    path('insert_oglas/', insert_oglas, name='insert_oglas'),
    path('deleteusr/', deleteusr, name='deleteusr'),
    path('PrihvatiOrg', prihvatiorg, name = 'prihvatiorg'),
    path('out/', out, name='out'),
    path('create_oglas', create_oglas, name='create_oglas'),
    path('OrganizatorPocetna', orgpoc, name='orgpoc'),
    path('pravljenjeOglasa', orgPravljenjeOglasa, name='pravljenjeOglasa'),
    path('orgPregledOglasa', org_pregled, name='orgPregledOglasa'),
    path('otkaziOglas', otkazi_oglas, name='otkazi_oglas'),
    path('zavrsiOglas', zavrsi_oglas, name='zavrsi_oglas'),
    path('updateStatus', update_status, name='update_status'),
    path('ocenjivanjeKorisnika', ocena_korisnika, name = 'ocena_korisnika'),
    path('rate/<int:idoglas>/<int:user_id>/', rate_user, name = 'rate_user'),


]