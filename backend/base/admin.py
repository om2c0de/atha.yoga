from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Invisible
from django.contrib import admin
from django.contrib.admin.forms import AdminAuthenticationForm

from server.settings import DEBUG


class CaptchaAdminAuthenticationForm(AdminAuthenticationForm):
    captcha = ReCaptchaField(widget=ReCaptchaV2Invisible)


if not DEBUG:
    admin.AdminSite.login_form = CaptchaAdminAuthenticationForm

