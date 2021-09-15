from django import template
from django.utils.safestring import mark_safe
from jaribio import utils
from accounts import constants as ACCOUNT_CONSTANTS
from quiz import constants as QUIZ_CONSTANTS
import logging
import re
import json

NAME_PATTERN = re.compile(r"[,.-_\\]")

logger = logging.getLogger(__name__)
register = template.Library()


@register.filter
def access_dict(_dict, key):
    if isinstance(_dict, dict) :
        return _dict.get(key, None)
    return None



@register.filter
def account_type_key(value):
    k,v = utils.find_element_by_value_in_tuples(value, ACCOUNT_CONSTANTS.ACCOUNT_TYPE)
    if k is None:
        logger.info(f"account_type_key: Could not found key  for value \"{value}\"")
        return value
    return k


@register.filter
def account_type_value(key):
    k,v = utils.find_element_by_key_in_tuples(key, ACCOUNT_CONSTANTS.ACCOUNT_TYPE)
    if v is None:
        logger.info(f"account_type_value: Could not found value  for key \"{key}\"")
        return key
    return v

@register.simple_tag
@register.filter
def splitize(value):
    if not isinstance(value, str):
        return value
    result = " ".join(NAME_PATTERN.split(value))
    return result

@register.simple_tag(takes_context=True)
def json_ld(context, structured_data):
    request = context['request']
    structured_data['url'] = request.build_absolute_uri()
    indent = '\n'
    dumped = json.dumps(structured_data, ensure_ascii=False, indent=True, sort_keys=True)
    script_tag = f"<script type=\"application/ld+json\">{indent}{dumped}{indent}</script>"
    return mark_safe(script_tag)



@register.filter
def quiz_type_value(key):
    k,v = utils.find_element_by_key_in_tuples(key, QUIZ_CONSTANTS.QUIZ_TYPES)
    if v is None:
        logger.info(f"quiz_type_value : Could not found value  for key \"{key}\"")
        return key
    return v
