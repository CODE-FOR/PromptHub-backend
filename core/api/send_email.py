import random
import string
from datetime import timedelta
from django.conf import settings
from django.utils import timezone
from django.core.mail import send_mail

from core.models.user import ConfirmCode

EFFECTIVE_DURATION = 30

def make_confirm_code(email: str):
    code = "".join(random.sample(string.ascii_letters + string.digits, 5))
    expire_at = timezone.now() + timedelta(minutes=EFFECTIVE_DURATION)
    if ConfirmCode.objects.filter(email=email).exists():
        confirm_code = ConfirmCode.objects.get(email=email)
        confirm_code.code = code
        confirm_code.expire_at = expire_at
        confirm_code.save()
    else:
        ConfirmCode.objects.create(email=email, code=code, expire_at=expire_at, is_used=False)
    return code

def send_sign_in_email(email: str):
    subject = "PromptHub Sign Up"
    message = f"您的注册验证码为：{make_confirm_code(email)}，请在{EFFECTIVE_DURATION}分钟内进行验证"
    send_mail(subject, message, from_email=settings.EMAIL_HOST_USER, recipient_list=[email])

def send_forget_password_email(email: str):
    subject = "PromptHub Forget Password"
    message = f"您的找回密码验证码为：{make_confirm_code(email)}，请在{EFFECTIVE_DURATION}分钟内进行验证"
    send_mail(subject, message, from_email=settings.EMAIL_HOST_USER, recipient_list=[email])