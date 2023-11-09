from django.db import models

# Create your models here.

class User(models.Model):
    iduser = models.AutoField(db_column='IdUser', primary_key=True)  # Field name made lowercase.
    mail = models.CharField(unique=True, max_length=64)
    ime = models.CharField(db_column='Ime', max_length=20)  # Field name made lowercase.
    prezime = models.CharField(db_column='Prezime', max_length=20)  # Field name made lowercase.
    password = models.CharField(max_length=20)
    telefon = models.CharField(max_length=20)
    datum = models.DateField()
    pol = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = 'user'

class Organizator(models.Model):
    idorg = models.OneToOneField('User', models.DO_NOTHING, db_column='IdOrg', primary_key=True)  # Field name made lowercase.
    jmbg = models.CharField(db_column='JMBG', unique=True, max_length=20)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'organizator'

class Admin(models.Model):
    idadmin = models.OneToOneField('User', models.DO_NOTHING, db_column='IdAdmin', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'admin'


class Korisnik(models.Model):
    idkor = models.OneToOneField('User', models.DO_NOTHING, db_column='IdKor', primary_key=True)  # Field name made lowercase.
    nivo = models.IntegerField(db_column='Nivo')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'korisnik'


class Oglas(models.Model):
    idoglas = models.AutoField(db_column='IdOglas', primary_key=True)  # Field name made lowercase.
    sport = models.CharField(db_column='Sport', max_length=20)  # Field name made lowercase.
    vreme = models.TimeField()
    datum = models.DateField()
    brigraca = models.IntegerField(db_column='BrIgraca')  # Field name made lowercase.
    lokacija = models.CharField(db_column='Lokacija', max_length=20)  # Field name made lowercase.
    gotov = models.IntegerField(db_column='Gotov')  # Field name made lowercase.
    idorg = models.ForeignKey('Organizator', models.DO_NOTHING, db_column='IdOrg')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'oglas'


class Ocena(models.Model):
    idocena = models.AutoField(db_column='IdOcena', primary_key=True)  # Field name made lowercase.
    idkor = models.ForeignKey(Korisnik, models.DO_NOTHING, db_column='IdKor')  # Field name made lowercase.
    ocena = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'ocena'








class PrijaveOrganizatora(models.Model):
    idprijave = models.AutoField(db_column='IdPrijave', primary_key=True)  # Field name made lowercase.
    mail = models.CharField(unique=True, max_length=64)
    ime = models.CharField(db_column='Ime', max_length=20)  # Field name made lowercase.
    prezime = models.CharField(db_column='Prezime', max_length=20)  # Field name made lowercase.
    telefon = models.CharField(max_length=20)
    datum = models.DateField()
    pol = models.IntegerField()
    jmbg = models.CharField(db_column='JMBG', unique=True, max_length=20)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'prijave_organizatora'


class PrijaveZaOglas(models.Model):
    idp = models.AutoField(db_column='IdP', primary_key=True)  # Field name made lowercase.
    idkor = models.ForeignKey(Korisnik, models.DO_NOTHING, db_column='IdKor')  # Field name made lowercase.
    status = models.IntegerField()
    idoglas = models.ForeignKey(Oglas, models.DO_NOTHING, db_column='IdOglas')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'prijave_za_oglas'







