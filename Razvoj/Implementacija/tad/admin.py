from django.contrib import admin
from .models import  *
# Register your models here.

admin.site.register(Korisnik)
admin.site.register(Organizator)
admin.site.register(Admin)
admin.site.register(Oglas)
admin.site.register(Ocena)
admin.site.register(PrijaveOrganizatora)
admin.site.register(PrijaveZaOglas)