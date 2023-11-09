##Andreja Vucic je radio sve vezano za organizatora
##Teodor Sutic je radio sve vezano za korisnika kao i log in i sve registracije
##Danilo Nikolic je radio sve vezano za Admina


from django.shortcuts import render, redirect

# Create your views here.
from django.http import HttpResponse, JsonResponse
from .models import *
from django.shortcuts  import render
from django.contrib.auth import authenticate, login,logout
from datetime import datetime
from django.contrib import messages

from .forms import *
#Pocetna strana ujedno i log in strana
def index(request):
    if request.method == 'POST':
        msg = ""
        form = LoginForm(request.POST)
        if form.is_valid():
            kor = 0
            mail = form.cleaned_data['username']
            password = form.cleaned_data['password']
            type = form.cleaned_data['userChoice']
            user = User.objects.filter(mail=mail).first()


            if user and password == user.password:

                if(type == 'kor' and Korisnik.objects.filter(idkor=user.iduser)):
                    request.session['user_id'] = user.iduser
                    request.session['kor'] = user.iduser
                    return redirect('korpoc')
                if(type == 'org' and Organizator.objects.filter(idorg=user.iduser)):
                    request.session['user_id'] = user.iduser
                    request.session['org'] = user.iduser
                    return redirect('orgpoc')
                    #stavite redirect gde vi zelite
                   #return redirect('korpoc')
                if (type == 'adm' and Admin.objects.filter(idadmin=user.iduser)):
                    request.session['user_id'] = user.iduser
                    request.session['adm'] = user.iduser
                    print("USAO")
                    return redirect('adminpoc')
                    # stavite redirect gde vi zelite
                    # return redirect('korpoc')
                msg += "Izabrali ste pogresnu vrstu korisnika\n"
                request.session['msg'] = msg
                return redirect('index')


            else:
                msg += "Mail ili lozinka su pogresni\n"
                request.session['msg'] = msg
                return redirect('index')
                #form.add_error(None, 'Invalid email or password.')

    else:
        msg = ""
        form = LoginForm()
        msg = request.session.pop('msg', '')
    context = {
        'form': form,
        'msg' : msg
    }
    return render(request, 'baza.html', context)

#Admin
def adminpoc(request):
     userd_id = request.session.get('user_id')
     amin_id =request.session.get('adm')
     user = User.objects.get(iduser = userd_id)
     if userd_id and amin_id:
         context = {
             'user':user
         }
         return render(request,'AdminPoc.html',context)
     else:
         return redirect('out')


def uklonikor(request):
    userd_id = request.session.get('user_id')
    amin_id = request.session.get('adm')
    user = User.objects.get(iduser=userd_id)
    if userd_id and amin_id:
        organizer_users = User.objects.filter(iduser__in=Organizator.objects.values('idorg'))
        korisnik_users = User.objects.filter(iduser__in=Korisnik.objects.values('idkor'))
        context = {
            'organizatori': organizer_users,
            'korisnici': korisnik_users,
            'user': user
        }
        return render(request, 'UkloniKorisnika.html', context)
    else:
        return redirect('out')

#Admin brisanje korisnika
def deleteusr(request):

    if request.method == 'POST':

        iduser = request.POST.get('iduser')
        try:
            user = User.objects.get(iduser=iduser)
            # Delete the user

            user.delete()
            return JsonResponse({'success': True})
        except User.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'User does not exist'})
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

#AdminPrihvatanje prijave
def prihvati(request):
    print("USAO")  # Debug statement to check if the view is accessed

    if request.method == 'POST':
        print("USAO POST")  # Debug statement to check if the request method is POST

        mail = request.POST.get('mail')
        jmbg = request.POST.get('jmbg')
        try:
            user = User.objects.get(mail=mail)
            pri = PrijaveOrganizatora.objects.get(mail=mail)
            prijava = Organizator(
                idorg_id=user.iduser,
                jmbg=jmbg
            )

            prijava.save()
            pri.delete()

            return JsonResponse({'success': True})
        except User.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'User does not exist'})
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

#AdminOdbijanjePrijave
def odbij(request):
    if request.method == 'POST':

        mail = request.POST.get('mail')

        try:
            user = User.objects.get(mail=mail)
            pri = PrijaveOrganizatora.objects.get(mail=mail)
            user.delete()
            pri.delete()

            return JsonResponse({'success': True})
        except User.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'User does not exist'})
    return JsonResponse({'success': False, 'message': 'Invalid request method'})



def prihvatiorg(request):
    userd_id = request.session.get('user_id')
    amin_id = request.session.get('adm')
    user = User.objects.get(iduser=userd_id)
    if userd_id and amin_id:
        prijave = PrijaveOrganizatora.objects.all()
        context = {
            'user': user,
            'prijave':prijave
        }
        return render(request, 'PrihvatanjeOrg.html', context)
    else:
        return redirect('out')




#Registracija korisnika
def regkor(request):
    poruka = ""
    if request.method == 'POST':
        # Retrieve form data
        ime = request.POST['ime']
        prezime = request.POST['prezime']
        passwd = request.POST['passwd']
        email = request.POST['email']
        phone = request.POST['phone']
        datum = request.POST['datum']
        pol = request.POST['pol']
        nivo = int(request.POST['categories'])
        user = User.objects.filter(mail = email)
        if(user):
            poruka+="Korisnik sa zadatim mailom vec postoji"
        else:
            new_user = User(
                mail=email,
                ime=ime,
                prezime=prezime,
                password=passwd,
                telefon=phone,
                datum=datum,
                pol=pol
            )
            new_user.save()
            if(new_user):
                new_kor = Korisnik(
                    idkor = new_user,
                    nivo = int(nivo)
                )
                new_kor.save()
            return redirect('index')
    context = {
        "poruka": poruka
    }
    return render(request, 'RegKor.html', context)

#registracija organizatora
def regorg(request):
    poruka = ""
    if request.method == 'POST':
        # Retrieve form data
        ime = request.POST['ime']
        prezime = request.POST['prezime']
        passwd = request.POST['passwd']
        email = request.POST['email']
        phone = request.POST['phone']
        datum = request.POST['datum']
        pol = int(request.POST['pol'])
        jmbg = request.POST['JMBG']
        user = User.objects.filter(mail=email)
        org = Organizator.objects.filter(jmbg = jmbg)
        prijavajmbg = PrijaveOrganizatora.objects.filter(jmbg=jmbg)
        prijava =PrijaveOrganizatora.objects.filter(mail=email)
        if(org or prijavajmbg):
            poruka += "Organizator ili prijava sa zadatim JMBG vec postoji\n"
        else:
            if (user or prijava):
                poruka += "Organizator ili prijava sa zadatim mailom vec postoji\n"
            else:
                r2=0
                if(pol == 1):
                    r2 = 'F'
                else:
                    r2 = 'M'
                new_user = User(
                    mail=email,
                    ime=ime,
                    prezime=prezime,
                    password=passwd,
                    telefon=phone,
                    datum=datum,
                    pol=r2
                )
                new_user.save()
                new_org = PrijaveOrganizatora(
                    mail=email,
                    ime=ime,
                    prezime=prezime,
                    jmbg=jmbg,
                    telefon=phone,
                    datum=datum,
                    pol=pol
                )
                new_org.save()
                return redirect('index')
    context = {
        "poruka": poruka
    }
    return render(request, 'RegOrg.html', context)

#Pocetna strana korisnika
def korpoc(request):
    user_id = request.session.get('user_id')
    kor = request.session.get('kor')

    if user_id and kor:
        user = User.objects.get(iduser=user_id)
        pr2 = PrijaveZaOglas.objects.filter(idkor=user_id, status=1)
        prijave = Oglas.objects.filter(idoglas__in=pr2.values('idoglas'), gotov = 0)
        ocena = Ocena.objects.filter(idkor = user_id)
        context = {
            'user_id': user_id,
            'user' : user,
            'prijave':prijave,
            'ocena' : ocena
        }

        return render(request, 'kortemp.html', context)
    else:
        return redirect('out')

#Pregled oglasa kod korisnika
def korpregled(request):
    user_id = request.session.get('user_id')
    kor = request.session.get('kor')
    b= 0
    if user_id and kor:
        b=1
    else:
        return redirect('out')
    oglas = Oglas.objects.filter(gotov = 0, brigraca__gt=0)
    user_id = request.session.get('user_id')
    prijave_list = PrijaveZaOglas.objects.filter(idkor=user_id)
    idoglas_values = prijave_list.values_list('idoglas', flat=True)
    filtered_oglas_list = oglas.exclude(idoglas__in=idoglas_values)

    context = {
        'oglas' : filtered_oglas_list
    }
    return render(request, 'pregledoglasa.html', context)
#Funkcija za prijavu oglasa kod korisnika-ne radi jos
def insert_oglas(request):
    try:

        card_id = request.POST.get('card_id')
        card_title = request.POST.get('card_title')
        iidb = 2

        user_id = request.session.get('user_id')
        korisnik = User.objects.get(iduser=user_id)
        oglas = Oglas.objects.get(idoglas = card_id)


        prijava = PrijaveZaOglas(
            idoglas_id= oglas.idoglas,
            idkor_id= korisnik.iduser,
            status=0
        )

        prijava.save()


        return JsonResponse({'status': 'success'})
    except:
        return JsonResponse({'status': 'error'})


#Logout view
def out(request):
    # Clear the user_id from the session
    if 'user_id' in request.session:
        del request.session['user_id']
    if 'kor' in request.session:
        del request.session['kor']
    if 'org' in request.session:
        del request.session['org']
    if 'adm' in request.session:
        del request.session['adm']



    # Redirect to the desired page after logout
    return redirect('index')


#Organizator deo


def orgpoc(request):
    user_id = request.session.get('user_id')
    org_id = request.session.get('org')
    oglasi = Oglas.objects.filter(gotov=0, idorg=org_id)
    b = 0
    if org_id:
        b = 1
    else:
        return redirect('out')

    # Create a dictionary to store oglas and corresponding applied users
    oglas_dict = {}
    '''
    TREBA DODATI DA SE PRIKAZUJE I AVG OCENA
    '''
    for oglas in oglasi:
        prijave = PrijaveZaOglas.objects.filter(idoglas=oglas, status=0)
        korisnici = Korisnik.objects.filter(idkor__in=prijave.values_list('idkor__idkor', flat=True))
        user_list = list(korisnici)  # Modify to include desired user information
        #tipa ovde dodam samo niz ocena i posaljem to kao deo contexta ne nuzno kao deo oglas_dict
        users = []
        for korisnik in korisnici:
            users.append(korisnik.idkor)
            print(korisnik.idkor.iduser)
        oglas_dict[oglas] = users

    print ("OGLAS_DICT: \n")
    print (oglas_dict)

    context = {
        'oglas_dict': oglas_dict,
    }

    return render(request, 'orgPocetna.html', context)

def ocena_korisnika(request):
    org = request.session.get('org')
    if org:
        b = 1
    else:
        return redirect('out')
    prijavljeni = PrijaveZaOglas.objects.filter(status = 1, idoglas__gotov = 1, idoglas__idorg = org)
    oglas_prijavljeni = {}

    for prijava in prijavljeni:
        idoglas = prijava.idoglas_id
        #print("IdOglas: " + str(idoglas) + "  IdUser: " + str(prijava.idkor.idkor))
        user_info = {
            'id':prijava.idkor.idkor.iduser,
            'name': f"{prijava.idkor.idkor.ime} {prijava.idkor.idkor.prezime}"
        }
        print(user_info)
        if idoglas in oglas_prijavljeni:
            oglas_prijavljeni[idoglas].append(user_info)
        else:
            oglas_prijavljeni[idoglas] = [user_info]

    print(oglas_prijavljeni)

    context = {'prijavljeni': oglas_prijavljeni}
    return render(request, 'ocenjivanjeKorisnika.html', context)
#kada je bez select_related vraca objekte prijava za idgolas 5 i 6


def rate_user(request, idoglas, user_id):
    if request.method == 'POST':
        rating = request.POST.get('rating')
        user = User.objects.get(iduser = user_id)
        korisnik = Korisnik.objects.get(idkor = user)
        print(korisnik)

        ocena = Ocena(idkor = korisnik, ocena = int(rating))
        ocena.save()

        prijava = PrijaveZaOglas.objects.get(idoglas= idoglas, idkor = korisnik)
        prijava.status = 3
        prijava.save()

    return redirect('orgpoc')

def orgPravljenjeOglasa(request):
    org_id = request.session.get('org')
    if org_id:
        b = 1
    else:
        return redirect('out')
    return render(request, 'pravljenjeOglasa.html')
def create_oglas(request):
    print("U create_oglas sam")
    if request.method == "POST":
        user_id = request.session.get('user_id')
        org = request.session.get('org')
        naziv_dogadjaja = request.POST.get('naziv')
        date = request.POST.get('date')
        ime_prezime = request.POST.get('name')
        lok = request.POST.get('location')
        sport = request.POST.get('sport')
        br_ljudi = request.POST.get('people')
        date_obj = datetime.strptime(date, '%Y-%m-%d').date()
        #Satro cuvam u bazi sad
        vreme = request.POST.get('vreme')
        organizator = Organizator.objects.get(idorg = org)
        oglas = Oglas(sport = sport, datum = date_obj, brigraca = int(br_ljudi), lokacija = lok, gotov = 0, idorg = organizator, vreme = vreme)

        oglas.save()
        messages.success(request, 'Oglas uspesno napravljen!')
        #return render(request, 'adminHome.html')
        return redirect('orgpoc')
    else:
        return redirect('index')


def org_pregled(request):
    user_id = request.session.get('user_id')
    org_id = request.session.get('org')
    oglasi = Oglas.objects.filter(gotov = 0, idorg = org_id)
    if org_id:
        b = 1
    else:
        return redirect('out')

    context = {
        'oglas' : oglasi
    }

    return render(request, 'orgPregledOglasa.html', context)

def otkazi_oglas(request):
    print('u otkazi oglas')
    try:
        oglas_id = request.POST.get('id_oglas')
        oglas = Oglas.objects.get(idoglas = oglas_id)
        oglas.gotov = 2
        oglas.save()
        return JsonResponse({'status' : 'success'})
    except:
        return JsonResponse({'status' : 'error'})

def update_status(request):
    print("u update statusu sam")
    if request.method == 'POST':
        oglas_id = request.POST.get('oglas_id')
        korisnik_id = request.POST.get('korisnik_id')

        status = request.POST.get('status')

        if (int(status) == 1):
            oglas = Oglas.objects.get(idoglas = oglas_id)
            oglas.brigraca -= 1
            oglas.save()

        print("Userid:" + korisnik_id + "   OglasId: " + oglas_id)
        #prijava = PrijaveZaOglas.objects.filter(idoglas_id=oglas_id, idkor_id=korisnik_id)
        prijava = PrijaveZaOglas.objects.get(idoglas_id = oglas_id, idkor_id = korisnik_id)
        prijava.status = status

        prijava.save()

    return JsonResponse({'message' : 'Prijava nije prosla'})

def zavrsi_oglas(request):
    print("u zavrsi oglasi")
    try:
        oglas_id = request.POST.get('id_oglas')
        oglas = Oglas.objects.get(idoglas = oglas_id)
        oglas.gotov = 1
        oglas.save()
        return JsonResponse({'status' : 'success'})
    except:
        return JsonResponse({'status' : 'error'})



#Amin


#Registracija korisnika
def regkor(request):
    poruka = ""
    if request.method == 'POST':
        # Retrieve form data
        ime = request.POST['ime']
        prezime = request.POST['prezime']
        passwd = request.POST['passwd']
        email = request.POST['email']
        phone = request.POST['phone']
        datum = request.POST['datum']
        pol = request.POST['pol']
        nivo = int(request.POST['categories'])
        user = User.objects.filter(mail = email)
        if(user):
            poruka+="Korisnik sa zadatim mailom vec postoji"
        else:
            new_user = User(
                mail=email,
                ime=ime,
                prezime=prezime,
                password=passwd,
                telefon=phone,
                datum=datum,
                pol=pol
            )
            new_user.save()
            if(new_user):
                new_kor = Korisnik(
                    idkor = new_user,
                    nivo = int(nivo)
                )
                new_kor.save()
            return redirect('index')
    context = {
        "poruka": poruka
    }
    return render(request, 'RegKor.html', context)

#registracija organizatora
def regorg(request):
    poruka = ""
    if request.method == 'POST':
        # Retrieve form data
        ime = request.POST['ime']
        prezime = request.POST['prezime']
        passwd = request.POST['passwd']
        email = request.POST['email']
        phone = request.POST['phone']
        datum = request.POST['datum']
        pol = int(request.POST['pol'])
        jmbg = request.POST['JMBG']
        user = User.objects.filter(mail=email)
        org = Organizator.objects.filter(jmbg = jmbg)
        prijavajmbg = PrijaveOrganizatora.objects.filter(jmbg=jmbg)
        prijava =PrijaveOrganizatora.objects.filter(mail=email)
        if(org or prijavajmbg):
            poruka += "Organizator ili prijava sa zadatim JMBG vec postoji\n"
        else:
            if (user or prijava):
                poruka += "Organizator ili prijava sa zadatim mailom vec postoji\n"
            else:
                r2=0
                if(pol == 1):
                    r2 = 'F'
                else:
                    r2 = 'M'
                new_user = User(
                    mail=email,
                    ime=ime,
                    prezime=prezime,
                    password=passwd,
                    telefon=phone,
                    datum=datum,
                    pol=r2
                )
                new_user.save()
                new_org = PrijaveOrganizatora(
                    mail=email,
                    ime=ime,
                    prezime=prezime,
                    jmbg=jmbg,
                    telefon=phone,
                    datum=datum,
                    pol=pol
                )
                new_org.save()
                return redirect('index')
    context = {
        "poruka": poruka
    }
    return render(request, 'RegOrg.html', context)


