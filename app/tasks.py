from django.core.mail import send_mail
from django.conf import settings

def send_scheduled_email(recipient_email, subject, message):
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[recipient_email],
            fail_silently=False,
        )
        return f"Email sent to {recipient_email}"
    
    except Exception as e:
        return f"Error sending email: {str(e)}"