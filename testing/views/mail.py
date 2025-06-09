from django.core.mail import send_mail
from django.http import HttpResponse
from django.conf import settings

def SendTestEmail(request):
    subject = 'Test E-posta'
    message = 'Bu bir test e-posta mesajıdır.'
    recipient_list = ['recipient@example.com'] 

    try:
        send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list)
        return HttpResponse('Test e-posta başarıyla gönderildi!', status=200)
    except Exception as e:
        return HttpResponse(f'E-posta gönderilemedi: {e}', status=500)
