from django import forms
from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.models import User

class RequestForm(forms.Form):

    request_question = forms.CharField(label='Poll Question', max_length=50, required=True)
    answer_option1 = forms.CharField(label='Answer 1', max_length=50, required=True)
    answer_option2 = forms.CharField(label='Answer 2', max_length=50, required=True)
    answer_option3 = forms.CharField(label='Answer 3', max_length=50)