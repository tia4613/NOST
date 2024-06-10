from allauth.account.adapter import DefaultAccountAdapter
from allauth.account.utils import user_field
from django.conf import settings
from django.urls import reverse


class CustomUserAccountAdapter(DefaultAccountAdapter):

    def save_user(self, request, user, form, commit=True):
        user = super().save_user(request, user, form, False)
        user_field(user, "nickname", request.data.get("nickname"))
        user.save()
        return user

    def send_confirmation_mail(self, request, emailconfirmation, signup):
        activate_url = reverse("account_confirm_email", args=[emailconfirmation.key])
        print(activate_url)
        activate_url = settings.SITE_URL + activate_url
        print(activate_url)
        ctx = {
            "user": emailconfirmation.email_address.user,
            "activate_url": activate_url,
            "key": emailconfirmation.key,
            "email": emailconfirmation.email_address.email,
        }
        if signup:
            email_template = "account/email/email_confirmation_signup"
        else:
            email_template = "account/email/email_confirmation"
        self.send_mail(email_template, emailconfirmation.email_address.email, ctx)
