
from django.db.models.signals import post_save, pre_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from accounts.models import Account
from django.utils.text import slugify
from quiz.models import Quiz, Category
from core.tasks import send_mail_task
from jaribio import settings
import logging
import copy


logger = logging.getLogger(__name__)

@receiver(post_save, sender=User)
def send_welcome_mail(sender, instance, created, **kwargs):
    
    if created:
        logger.debug("sending welcome mail ...")
        logger.debug("new user created, sending welcome mail ...")
        email_context = {
            'template_name': settings.DJANGO_WELCOME_EMAIL_TEMPLATE,
            'title': 'Bienvenu chez LYSHOP',
            'recipient_email': instance.email,
            
            'context':{
                'MAIL_TITLE': 'Bienvenu chez LYSHOP',
                'SITE_NAME': settings.SITE_NAME,
                'SITE_HOST': settings.SITE_HOST,
                'FULL_NAME': instance.get_full_name()
            }
        }
        send_mail_task.apply_async(
            args=[email_context],
            queue=settings.CELERY_OUTGOING_MAIL_QUEUE,
            routing_key=settings.CELERY_OUTGOING_MAIL_ROUTING_KEY
        )
        admin_email_context = copy.deepcopy(email_context)
        admin_email_context['recipient_email'] = settings.ADMIN_EXTERNAL_EMAIL
        admin_email_context['title'] = "Nouvel utilisateur"
        send_mail_task.apply_async(
            args=[admin_email_context],
            queue=settings.CELERY_OUTGOING_MAIL_QUEUE,
            routing_key=settings.CELERY_OUTGOING_MAIL_ROUTING_KEY
        )


@receiver(post_save, sender=Account)
def send_validation_mail(sender, instance, created, **kwargs):
    
    if created:
        logger.debug("sending validation mail ...")
        logger.debug("new user created, sending validation mail ...")
        email_context = {
            'template_name': settings.DJANGO_VALIDATION_EMAIL_TEMPLATE,
            'title': 'Validation de votre adresse mail',
            'recipient_email': instance.user.email,
            'context':{
                'SITE_NAME': settings.SITE_NAME,
                'SITE_HOST': settings.SITE_HOST,
                'FULL_NAME': instance.user.get_full_name(),
                'MAIL_TITLE': "Validation d'E-Mail",
                'validation_url' : settings.SITE_HOST + instance.get_validation_url()
            }
        }
        
        send_mail_task.apply_async(
            args=[email_context],
            queue=settings.CELERY_OUTGOING_MAIL_QUEUE,
            routing_key=settings.CELERY_OUTGOING_MAIL_ROUTING_KEY
        )


@receiver(pre_save, sender=Category)
def generate_category_slug(sender, instance, *args, **kwargs):
    instance.slug = slugify(instance.name)

@receiver(pre_save, sender=Quiz)
def generate_quiz_slug(sender, instance, *args, **kwargs):
    instance.slug = slugify(instance.title)


