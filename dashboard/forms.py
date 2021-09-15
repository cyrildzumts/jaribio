from django import forms
from django.contrib.auth.models import Group, Permission
from django.utils import timezone
from dashboard.models import PartnerToken
from accounts.models import Account

import datetime


class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ("user","date_of_birth","telefon",
                  "newsletter","account_type",
                  "email_validated", )
        


class TokenForm(forms.Form):
    user = forms.IntegerField()


class GroupFormCreation(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'permissions']



class PartnerTokenForm(forms.ModelForm):

    class Meta:
        model = PartnerToken
        fields = PartnerToken.FORM_FIELDS