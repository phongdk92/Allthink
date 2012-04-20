import re
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.forms.widgets import *


class LoginForm(forms.Form) :
    username = forms.CharField(label="Username", max_length=30)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

class RegistrationForm(forms.Form):
    username = forms.CharField(label='Username', max_length=30)
    email = forms.EmailField(label='Email')
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput()
    )
    password2 = forms.CharField(
        label='Password (Again)',
        widget=forms.PasswordInput()
    )

    fullname = forms.CharField (label='Your name', max_length=30)

    def clean_username(self):
        username = self.cleaned_data['username']
        if not re.search(r'^\w+$', username):
            raise forms.ValidationError('Username can only containal phanumeric characters and the underscore.')
        try:
            User.objects.get(username=username)
        except ObjectDoesNotExist:
            return username
        raise forms.ValidationError('Username is already taken.')

    def clean_password2(self):
        if 'password1' in self.cleaned_data:
            password1 = self.cleaned_data['password1']
            password2 = self.cleaned_data['password2']
            if password1 == password2:
                return password2
        raise forms.ValidationError('Passwords do not match.')

class EditAccountForm(forms.Form):
    username = forms.CharField(label='Username', widget= TextInput(attrs={'readonly':'readonly', 'disabled' : 'disabled'}), max_length=30)
    email = forms.EmailField(label='Email', widget= TextInput(attrs={'readonly':'readonly', 'disabled' : 'disabled'}))
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput()
    )
    password2 = forms.CharField(
        label='Password (Again)',
        widget=forms.PasswordInput()
    )

    password0 = forms.CharField(
        label='Current password',
        widget=forms.PasswordInput()
    )

    fullname = forms.CharField (label='Your name', max_length=30)

    def clean_password2(self):
        if 'password1' in self.cleaned_data:
            password1 = self.cleaned_data['password1']
            password2 = self.cleaned_data['password2']
            if password1 == password2:
                return password2
        raise forms.ValidationError('Passwords do not match.')

class CreateLesson(forms.Form) :
    #
    lessonTitle = forms.CharField(label="Lesson title", max_length=100)
    GRADE_LEVEL = (
        ('all','All grade level') ,
        ('e' , 'Elementary') ,
        ('h' , 'High school') ,
        ('c' , 'College')
    )
    gradeLevel = forms.ChoiceField(label="Grade level", widget= Select, choices= GRADE_LEVEL)
    SUBJECT = (
        ('math', 'Math'),
        ('science', 'Science'),
        ('physic', 'Physic')
    )
    subject = forms.ChoiceField(label="Subject", widget= Select  , choices = SUBJECT)
    description = forms.CharField(label="description", widget= Textarea(attrs={'cols': 70, 'rows': 5, 'style' : 'resize: none;'}), max_length=2000)


class AddVideoForm(forms.Form):
    pageTitle = forms.CharField(label= 'pageTitle', max_length=100)
    url = forms.URLField(label='url')
    text = forms.CharField(label="text", widget= Textarea(attrs={'cols': 70, 'rows': 5, 'style' : 'resize: none;'}), max_length=2000 , required= False)


class AddDocumentForm(forms.Form):
    pageTitle = forms.CharField(label= 'pageTitle', max_length=100, required= False)
    FILES = (
        ('non', 'non'),
        )
    selectFile = forms.ChoiceField(label="selectFile", widget= Select  , choices = FILES, required= False)
    text = forms.CharField(label="text", widget= Textarea(attrs={'cols': 70, 'rows': 5, 'style' : 'resize: none;'}), max_length=2000, required= False)


class AddImageForm(forms.Form):
    pageTitle = forms.CharField(label= 'pageTitle', max_length=100)
    FILES = (
        )
    selectFile = forms.ChoiceField(label="selectFile", widget= Select  , choices = FILES, required= False)
    text = forms.CharField(label="text", widget= Textarea(attrs={'cols': 70, 'rows': 5, 'style' : 'resize: none;'}), max_length=2000, required= False)

class AddStepbyStepForm(forms.Form):
    pageTitle = forms.CharField(label= 'pageTitle', max_length=100)
    promt = forms.CharField(label= 'promt', widget= Textarea(attrs={'cols': 65, 'rows': 4, 'style' : 'resize: none;'}), max_length=300)
    step1 = forms.CharField(label= 'step1', widget= Textarea(attrs={'cols': 30, 'rows': 1, 'style' : 'resize: none;'}), max_length=100, required=False)
    explain1 = forms.CharField(label= 'Explaination', widget= Textarea(attrs={'cols': 30, 'rows': 1, 'style' : 'resize: none;'}), max_length=100, required=False)
    step2 = forms.CharField(label= 'step2', widget= Textarea(attrs={'cols': 30, 'rows': 1, 'style' : 'resize: none;'}), max_length=100, required=False)
    explain2 = forms.CharField(label= 'Explaination', widget= Textarea(attrs={'cols': 30, 'rows': 1, 'style' : 'resize: none;'}), max_length=100, required=False)
    step3 = forms.CharField(label= 'step3', widget= Textarea(attrs={'cols': 30, 'rows': 1, 'style' : 'resize: none;'}), max_length=100, required=False)
    explain3 = forms.CharField(label= 'Explaination', widget= Textarea(attrs={'cols': 30, 'rows': 1, 'style' : 'resize: none;'}), max_length=100, required=False)
    step4 = forms.CharField(label= 'step4', widget= Textarea(attrs={'cols': 30, 'rows': 1, 'style' : 'resize: none;'}), max_length=100, required=False)
    explain4 = forms.CharField(label= 'Explaination', widget= Textarea(attrs={'cols': 30, 'rows': 1, 'style' : 'resize: none;'}), max_length=100, required=False)
    step5 = forms.CharField(label= 'step5', widget= Textarea(attrs={'cols': 30, 'rows': 1, 'style' : 'resize: none;'}), max_length=100, required=False)
    explain5 = forms.CharField(label= 'Explaination', widget= Textarea(attrs={'cols': 30, 'rows': 1, 'style' : 'resize: none;'}), max_length=100, required=False)
    step6 = forms.CharField(label= 'step6', widget= Textarea(attrs={'cols': 30, 'rows': 1, 'style' : 'resize: none;'}), max_length=100, required=False)
    explain6 = forms.CharField(label= 'Explaination', widget= Textarea(attrs={'cols': 30, 'rows': 1, 'style' : 'resize: none;'}), max_length=100, required=False)
    step7 = forms.CharField(label= 'step7', widget= Textarea(attrs={'cols': 30, 'rows': 1, 'style' : 'resize: none;'}), max_length=100, required=False)
    explain7 = forms.CharField(label= 'Explaination', widget= Textarea(attrs={'cols': 30, 'rows': 1, 'style' : 'resize: none;'}), max_length=100, required=False)
    step8 = forms.CharField(label= 'step8', widget= Textarea(attrs={'cols': 30, 'rows': 1, 'style' : 'resize: none;'}), max_length=100, required=False)
    explain8 = forms.CharField(label= 'Explaination', widget= Textarea(attrs={'cols': 30, 'rows': 1, 'style' : 'resize: none;'}), max_length=100, required=False)
    step9 = forms.CharField(label= 'step9', widget= Textarea(attrs={'cols': 30, 'rows': 1, 'style' : 'resize: none;'}), max_length=100, required=False)
    explain9 = forms.CharField(label= 'Explaination', widget= Textarea(attrs={'cols': 30, 'rows': 1, 'style' : 'resize: none;'}), max_length=100, required=False)
    step10 = forms.CharField(label= 'step10', widget= Textarea(attrs={'cols': 30, 'rows': 1, 'style' : 'resize: none;'}), max_length=100, required=False)
    explain10 = forms.CharField(label= 'Explaination', widget= Textarea(attrs={'cols': 30, 'rows': 1, 'style' : 'resize: none;'}), max_length=100, required=False)
    step11 = forms.CharField(label= 'step11', widget= Textarea(attrs={'cols': 30, 'rows': 1, 'style' : 'resize: none;'}), max_length=100, required=False)
    explain11 = forms.CharField(label= 'Explaination', widget= Textarea(attrs={'cols': 30, 'rows': 1, 'style' : 'resize: none;'}), max_length=100, required=False)
    step12 = forms.CharField(label= 'step12', widget= Textarea(attrs={'cols': 30, 'rows': 1, 'style' : 'resize: none;'}), max_length=100, required=False)
    explain12 = forms.CharField(label= 'Explaination', widget= Textarea(attrs={'cols': 30, 'rows': 1, 'style' : 'resize: none;'}), max_length=100, required=False)
    step13 = forms.CharField(label= 'step13', widget= Textarea(attrs={'cols': 30, 'rows': 1, 'style' : 'resize: none;'}), max_length=100, required=False)
    explain13 = forms.CharField(label= 'Explaination', widget= Textarea(attrs={'cols': 30, 'rows': 1, 'style' : 'resize: none;'}), max_length=100, required=False)
    step14 = forms.CharField(label= 'step14', widget= Textarea(attrs={'cols': 30, 'rows': 1, 'style' : 'resize: none;'}), max_length=100, required=False)
    explain14 = forms.CharField(label= 'Explaination', widget= Textarea(attrs={'cols': 30, 'rows': 1, 'style' : 'resize: none;'}), max_length=100, required=False)
    step15 = forms.CharField(label= 'step15', widget= Textarea(attrs={'cols': 30, 'rows': 1, 'style' : 'resize: none;'}), max_length=100, required=False)
    explain15 = forms.CharField(label= 'Explaination', widget= Textarea(attrs={'cols': 30, 'rows': 1, 'style' : 'resize: none;'}), max_length=100, required=False)
    step16 = forms.CharField(label= 'step16', widget= Textarea(attrs={'cols': 30, 'rows': 1, 'style' : 'resize: none;'}), max_length=100, required=False)
    explain16 = forms.CharField(label= 'Explaination', widget= Textarea(attrs={'cols': 30, 'rows': 1, 'style' : 'resize: none;'}), max_length=100, required=False)
    step17 = forms.CharField(label= 'step17', widget= Textarea(attrs={'cols': 30, 'rows': 1, 'style' : 'resize: none;'}), max_length=100, required=False)
    explain17 = forms.CharField(label= 'Explaination', widget= Textarea(attrs={'cols': 30, 'rows': 1, 'style' : 'resize: none;'}), max_length=100, required=False)
    step18 = forms.CharField(label= 'step18', widget= Textarea(attrs={'cols': 30, 'rows': 1, 'style' : 'resize: none;'}), max_length=100, required=False)
    explain18 = forms.CharField(label= 'Explaination', widget= Textarea(attrs={'cols': 30, 'rows': 1, 'style' : 'resize: none;'}), max_length=100, required=False)
    step19 = forms.CharField(label= 'step19', widget= Textarea(attrs={'cols': 30, 'rows': 1, 'style' : 'resize: none;'}), max_length=100, required=False)
    explain19 = forms.CharField(label= 'Explaination', widget= Textarea(attrs={'cols': 30, 'rows': 1, 'style' : 'resize: none;'}), max_length=100, required=False)
    step20 = forms.CharField(label= 'step20', widget= Textarea(attrs={'cols': 30, 'rows': 1, 'style' : 'resize: none;'}), max_length=100, required=False)
    explain20 = forms.CharField(label= 'Explaination', widget= Textarea(attrs={'cols': 30, 'rows': 1, 'style' : 'resize: none;'}), max_length=100, required=False)

class AddTextForm(forms.Form):
    pageTitle = forms.CharField(label= 'pageTitle', max_length=100)
    text = forms.CharField(label="text", widget= Textarea(attrs={'cols': 70, 'rows': 5, 'style' : 'resize: none;'}), max_length=2000, required= False)

class FileUploadForm(forms.Form) :
    uploadFile = forms.FileField(
        label = 'uploadFile'
    )
