from datetimewidget.widgets import DateTimeWidget
from django import forms
# class UserRegistrationForm(forms.Form):
#     phone_number = forms.CharField(
#         required = True,
#         label = '',
#         max_length = 32
#     )
#     first_name = forms.CharField(
#         required = True,
#         label = 'Email',
#         max_length = 32,
#     )
#     last_name = forms.CharField(
#         required = True,
#         label = 'Password',
#         max_length = 32,
#         widget = forms.PasswordInput()
#     )
#     type = forms.ChoiceField()
from django.contrib.auth.forms import AuthenticationForm
from django.forms import ModelForm, SelectDateWidget

from worker.models import User, WorkerProfile, WorkerSkill, ContractorProfile, HireWorker


class UserRegistrationForm(ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'type', 'phone_number', 'email']

class LoginForm(forms.Form):

    phone_number = forms.RegexField(regex=r'^\d{10,15}$', error_messages={
            'invalid': ("please enter valid mobile number"),
            'unique': ("My message for unique") # <- THIS
        })
    password = forms.CharField(label = 'password', widget = forms.PasswordInput)

class ProfileForm(ModelForm):
    about = forms.CharField(widget = forms.Textarea({'cols': '30', 'rows': '10'}))
    class Meta:
        model = WorkerProfile
        exclude = ('user',)

class  ContractorProfileForm(ModelForm):

    class Meta:
        model =  ContractorProfile
        exclude = ('user',)

class  WorkerSkillForm(ModelForm):
    class Meta:
        model =  WorkerSkill
        exclude =('user', 'hired_by','status')
        widgets = {
            # Use localization and bootstrap 3
            'datetime': DateTimeWidget(attrs={'id': "from_date"}, usel10n=True, bootstrap_version=3)
        }

class HireSkillForm(ModelForm):
    to_date = forms.DateField(
        widget=SelectDateWidget(
            empty_label=("Choose Year", "Choose Month", "Choose Day"),
        ),
    )
    from_date = forms.DateField(
        widget=SelectDateWidget(
            empty_label=("Choose Year", "Choose Month", "Choose Day"),

        ),
    )

    class Meta:
        model = HireWorker
        fields =('from_date', 'to_date')
