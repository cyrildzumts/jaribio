from django.core.exceptions import ObjectDoesNotExist
from dashboard.forms import PartnerTokenForm
from dashboard.models import PartnerToken
import logging
import uuid


logger = logging.getLogger(__name__)

def create_partner_token(data):
    form = PartnerTokenForm(data)
    p_token = None
    if form.is_valid():
        p_token = form.save()
        logger.info(f"Created PartnerToken {p_token.name}")
    else:
        logger.warn(f"PartnerTokenForm is invald : errors : {form.errors}")
    
    return p_token

def update_partner_token(p_token, data):
    form = PartnerTokenForm(data, instance=p_token)
    updated = False
    if form.is_valid():
        p_token = form.save()
        updated = True
        logger.info(f"Updated PartnerToken {p_token.name}")
    else:
        logger.warn(f"PartnerTokenForm is invald : errors : {form.errors}")
    return p_token, updated


def get_partner_totken(partner):
    try:
        p_token = PartnerToken.objects.get(partner=partner)
        return p_token
    except ObjectDoesNotExist:
        return None

def get_partner_tokens():
    return PartnerToken.objects.all()