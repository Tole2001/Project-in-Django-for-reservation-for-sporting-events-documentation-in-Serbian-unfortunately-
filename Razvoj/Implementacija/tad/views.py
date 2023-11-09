from django.shortcuts import render, redirect
from datetime import datetime
# Create your views here.
from django.http import HttpResponse, JsonResponse
from .models import *
from django.shortcuts  import render
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout

from .forms import *
#Pocetna strana ujedno i log in strana
def index(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():

            mail = form.cleaned_data['username']
            password = form.cleaned_data['password']
            type = form.cleaned_data['userChoice']
            user = User.objects.filter(mail=mail).first()

            if user and password == user.password:
                request.session['user_id'] = user.iduser
                if(type == 'kor'):
                    request.session['kor'] = user.iduser
                    return redirect('korpoc')
                if(type == 'org'):
                    request.session['org'] = user.iduser
                    #stavite redirect gde vi zelite
                    #return redirect('create_oglas')
                    #return render(request, 'pravljenjeOglasa.html')
                    return redirect('orgpoc')
                if (type == 'adm'):
                    request.session['adm'] = user.iduser
                    # stavite redirect gde vi zelite
                # return redirect('korpoc')


            else:
                print("USAO " + mail + " " + password)
                form.add_error(None, 'Invalid email or password.')
    else:
        form = LoginForm()
    context = {
        'form': form
    }
    return render(request, 'baza.html', context)

#Registracija korisnika
def regkor(request):
    return render(request, 'Regkor.html')

#Pocetna strana korisnika
def korpoc(request):
    user_id = request.session.get('user_id')
    kor = request.session.get('kor')
    context = {
        'user_id': user_id
    }
    if user_id and kor:
        return render(request, 'kortemp.html',context)
    else:
        return redirect('out')

#Pocetna strana kod ogranizatora
def orgpoc(request):
    user_id = request.session.get('user_id')
    org = request.session.get('org')
    return render(request, 'orgPocetna.html')

def orgPravljenjeOglasa(request):
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



#Pregled oglasa kod korisnika
def korpregled(request):
    oglas = Oglas.objects.all()
    context = {
        'oglas' : oglas
    }
    return render(request, 'pregledoglasa.html',context)
#Funkcija za prijavu oglasa kod korisnika-ne radi jos
def insert_oglas(request):
    try:
        card_id = request.POST.get('card_id')
        card_title = request.POST.get('card_title')
        iidb = 2
        sts = 0
        PrijaveZaOglas.objects.create(idkor_id=iidb, idoglas=card_id, status=sts)
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
