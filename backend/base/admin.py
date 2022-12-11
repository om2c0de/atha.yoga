from django.contrib import admin
from django.contrib.admin.forms import AdminAuthenticationForm
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Invisible


class CaptchaAdminAuthenticationForm(AdminAuthenticationForm):
    captcha = ReCaptchaField(widget=ReCaptchaV2Invisible)


admin.AdminSite.login_form = CaptchaAdminAuthenticationForm
