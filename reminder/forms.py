from django.forms import ModelForm
from django import forms
from .models import Remind, RemindUser


class DateInput(forms.DateInput):
    input_type = 'date'

class RemindForm(ModelForm):
    class Meta:
        model = Remind
        fields = ('title', 'remind_date', 'remind_time',)
        widgets = {'remind_date': DateInput(),
                   'remind_time': forms.TimeInput(attrs={'type': 'time'}),
                   'title': forms.Textarea(attrs={'rows': 3, 'style': 'font-size: large',})
                   }

class RemindUserForm(ModelForm):
    class Meta:
        model = RemindUser
        fields = ('phonenumber', 'password1', 'password2',)
        widgets = {
            'phonenumber': forms.TextInput(attrs={'style': 'font-size: large', 'placeholder': '+98 765 432 123'}),
            'password1': forms.PasswordInput(),
            'password2': forms.PasswordInput(),
        }