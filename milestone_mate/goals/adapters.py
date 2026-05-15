from allauth.account.adapter import DefaultAccountAdapter
from django.forms import ValidationError

class GmailEnforceAdapter(DefaultAccountAdapter):
    def clean_email(self, email):
        if not email.lower().endswith('@gmail.com'):
            raise ValidationError("Please use a @gmail.com address to sign up.")
        return super().clean_email(email)
