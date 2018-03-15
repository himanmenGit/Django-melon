from django.conf import settings
from django.shortcuts import render
from django.core.mail import EmailMessage

__all__ = (
    'send_email',
)


def send_email(request):
    context = dict()
    if request.method == 'POST':
        # settings.EMAIL_HOST_USER = request.POST.get('me')
        # settings.EMAIL_HOST_PASSWORD = request.POST.get('password')
        email = EmailMessage(
            request.POST.get('title'),
            request.POST.get('body'),
            to=[request.POST.get('to_mail')],
        )
        if email:
            context['send_result'] = email.send()
    return render(request, 'email/email_send.html', context)