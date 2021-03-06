from django.core.mail import send_mail
from celery import shared_task
from django.template.loader import render_to_string
from quiz.models import Category
from jaribio import settings



import logging


logger = logging.getLogger(__name__)

@shared_task
def send_mail_task(email_context=None):
    logger.info("Send mail task called")
    # TODO : make sending email based on Django Template System.
    if email_context is not None and isinstance(email_context, dict):
        logger.debug("email_context available. Running send_mail now")
        try:
            template_name = email_context['template_name']
        except KeyError as e:
            logger.error(f"send_mail_task : template_name not available. Mail not send. email_context : {email_context}")
            return
        #message = loader.render_to_string(template_name, {'email': email_context})
        root_categories = Category.objects.filter(is_active=True)
        context = email_context['context']
        context['root_categories'] = root_categories
        html_message = render_to_string(template_name, context)
        send_mail(
            email_context['title'],
            None,
            settings.DEFAULT_FROM_EMAIL,
            [email_context['recipient_email']],
            html_message=html_message
        )
    else:
        logger.warn(f"send_mail_task: email_context missing or is not a dict. email_context : {email_context}")

    logger.info("Send mail task finished")

    