from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'lgn','placeholder': 'E-mail'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'lgn','placeholder': 'Lozinka'}))
    user_choices = [
        ('kor', 'Korisnik'),
        ('adm', 'Admin'),
        ('org', 'Organizator'),
        # add more choices here
    ]
    userChoice = forms.ChoiceField(choices=user_choices, widget=forms.Select(attrs={'class': 'lgn', 'style': 'width: 100%'}))
