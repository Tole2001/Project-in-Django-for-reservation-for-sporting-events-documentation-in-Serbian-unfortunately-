from django.test import TestCase, Client
from django.urls import reverse
from datetime import datetime

# Create your tests here.

from .models import *





class OrganizatorTest(TestCase):


            #Ocenjivanje Korisnika
            def test_rate_user(self):
                # Pravi user
                user = User.objects.create(
                    mail="email@gmail.com",
                    ime="ime",
                    prezime="prezime",
                    password="Passwd123",
                    telefon="0637596525",
                    datum="2023-04-26",
                    pol='M'
                )

                # Pravni Kor
                korisnik = Korisnik.objects.create(idkor=user.iduser,nivo= 3)

                #Pravi se org
                user2 = User.objects.create(
                    mail="email@gmail.com",
                    ime="ime2",
                    prezime="prezime2",
                    password="Passwd123",
                    telefon="0637596525",
                    datum="2023-04-26",
                    pol='M'
                )
                organizator = Organizator.objects.create(idorg=user2.iduser,jmbg="1111111111111")
                #Pravi Oglas
                oglas = Oglas.objects.create(
                    sport="soccer",
                    datum="2023-04-15",
                    brigraca=5,
                    lokacija="lok",
                    gotov=0,
                    idorg=organizator.idorg,
                    vreme="13:30:21"
                )
                # Pravi Prijavu za oglas
                prijava = PrijaveZaOglas.objects.create(idoglas=oglas.idoglas, idkor=korisnik.idkor,status=1)

                # Simulira Post
                response = self.client.post(reverse('rate_user'), {'rating': '5', 'user_id': korisnik.idkor})

                # Odgovor
                self.assertRedirects(response, '/orgpoc/')

                # Provera ocene
                ocena = Ocena.objects.get(idkor=korisnik.idkor)
                self.assertEqual(ocena.ocena, 5)
                prijava.refresh_from_db()
                self.assertEqual(prijava.status, 3)
            #Pravljenje oglasa
            def test_create_oglas(self):
                user4 = User.objects.create(
                    mail="email1231@gmail.com",
                    ime="ime4",
                    prezime="prezime4",
                    password="Passwd123",
                    telefon="0637596525",
                    datum="2023-04-26",
                    pol='M'
                )
                organizator4 = Organizator.objects.create(idorg=user4.iduser, jmbg="1111111111181")
                self.client.post(reverse('index'), {'username': 'email1231@gmail.com', 'password': 'Passwd123',
                                                               'userChoice': 'org'})

                url = reverse('create_oglas')
                date = datetime.now().strftime('%Y-%m-%d')
                response = self.client.post(url, {'naziv': 'Test Oglas', 'date': date, 'name': 'Idk',
                                                  'location': 'Test lokacija', 'sport': 'soccer',
                                                  'people': '5', 'vreme': '10:00'})

                # Assert that the response is a redirect
                self.assertRedirects(response, reverse('orgpoc'))

                # Check if the Oglas object was created with the correct attributes
                oglas = Oglas.objects.get(lokacija="Test lokacija")
                self.assertEqual(oglas.brigraca, 5)
                self.assertEqual(oglas.sport, 'soccer')
            #Neuspesno pravljenje oglasa
            def test_create_oglas_neuspeh(self):
                url = reverse('create_oglas')
                response = self.client.get(url)

                # Assert that the response is a redirect
                self.assertRedirects(response, reverse('index'))

                # Check that no Oglas objects were created
                self.assertFalse(Oglas.objects.exists())

            def test_otkazi_oglas_success(self):
                # Pravi se org
                user2 = User.objects.create(
                    mail="email5@gmail.com",
                    ime="ime2",
                    prezime="prezime5",
                    password="Passwd125",
                    telefon="0637596525",
                    datum="2023-04-26",
                    pol='M'
                )
                organizator = Organizator.objects.create(idorg=user2.iduser, jmbg="1111115111111")
                # Pravi Oglas
                oglas = Oglas.objects.create(
                    sport="soccer",
                    datum="2023-04-15",
                    brigraca=5,
                    lokacija="lok",
                    gotov=0,
                    idorg=organizator.idorg,
                    vreme="13:30:21"
                )
                client = Client()
                response = client.post(reverse('otkazi_oglas'), {'id_oglas': oglas.idoglas})

                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.json(), {'status': 'success'})


                oglas = Oglas.objects.get(idoglas=oglas.idoglas)
                self.assertEqual(oglas.gotov, 2)

            def test_zavrsi_oglas_success(self):
                # Pravi se org
                user2 = User.objects.create(
                    mail="email6@gmail.com",
                    ime="ime6",
                    prezime="prezime6",
                    password="Passwd1256",
                    telefon="0637596525",
                    datum="2023-04-26",
                    pol='M'
                )
                organizator = Organizator.objects.create(idorg=user2.iduser, jmbg="1121115111111")
                # Pravi Oglas
                oglas = Oglas.objects.create(
                    sport="soccer",
                    datum="2023-04-15",
                    brigraca=5,
                    lokacija="lok",
                    gotov=0,
                    idorg=organizator.idorg,
                    vreme="13:30:21"
                )
                client = Client()
                response = client.post(reverse('zavrsi_oglas'), {'id_oglas': oglas.idoglas})

                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.json(), {'status': 'success'})

                # Check that the Oglas object was updated
                oglas = Oglas.objects.get(idoglas=oglas.idoglas)
                self.assertEqual(oglas.gotov, 1)

            def test_update_status_success(self):
                user = User.objects.create(
                    mail="email99@gmail.com",
                    ime="ime1",
                    prezime="prezime1",
                    password="Passwd1223",
                    telefon="0637596525",
                    datum="2023-04-26",
                    pol='M'
                )

                # Pravni Kor
                korisnik = Korisnik.objects.create(idkor=user.iduser, nivo=3)
                user2 = User.objects.create(
                    mail="email67@gmail.com",
                    ime="ime67",
                    prezime="prezime67",
                    password="Passwd12567",
                    telefon="0637596525",
                    datum="2023-04-26",
                    pol='M'
                )
                organizator = Organizator.objects.create(idorg=user2.iduser, jmbg="7121115111111")
                # Pravi Oglas
                oglas = Oglas.objects.create(
                    sport="soccer",
                    datum="2023-04-15",
                    brigraca=8,
                    lokacija="lok",
                    gotov=0,
                    idorg=organizator.idorg,
                    vreme="13:30:21"
                )
                prijava = PrijaveZaOglas.objects.create(idoglas=oglas.idoglas, idkor=korisnik.idkor, status=0)
                client = Client()
                response = client.post(reverse('update_status'), {
                    'oglas_id': oglas.idoglas,
                    'korisnik_id': korisnik.idkor,
                    'status': '1'
                })

                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.json(), {'message': 'Prijava nije prosla'})



                # Da li je prijava updated
                prijava = PrijaveZaOglas.objects.get(idoglas=oglas.idoglas, idkor=korisnik.idkor)
                self.assertEqual(prijava.status, '1')


