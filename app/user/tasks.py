from celery import shared_task
from email.mime.image import MIMEImage
from django.contrib.staticfiles import finders
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives


@shared_task
def send_welcome_email_task(**kwargs):
    subject = kwargs['subject']
    from_email = 'zeed630@gmail.cl'
    to = kwargs['email']
    email_context = {
        'user_name': kwargs['name'], 
        'user_email': kwargs['email'], 
        'subject': subject
        }
    text_content = "Thank you for depositing the amount of"
    html = get_template('welcome_email.html')
    html_content = html.render(email_context)
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    return None


