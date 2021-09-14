from django.shortcuts import render, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import auth
from django.templatetags.static import static
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext as _
from django.contrib.sitemaps import Sitemap
# from django import forms
from django.contrib.auth.forms import UserCreationForm
from jaribio import settings
from django.utils import timezone
import datetime

import logging

logger = logging.getLogger(__name__)

def page_not_found(request):
    template_name = '404.html'
    return render(request, template_name)


def server_error(request):
    template_name = '500.html'
    return render(request, template_name)

def permission_denied(request):
    template_name = '500.html'
    return render(request, template_name)

def bad_request(request):
    template_name = '500.html'
    return render(request, template_name)


def home(request):
    """
    This function serves the About Page.
    By default the About html page is saved
    on the root template folder.
    """
    template_name = "home.html"
    page_title = settings.HOME_TITLE
    context = {
        'page_title': page_title,
        'user_is_authenticated' : request.user.is_authenticated,
        'OG_TITLE' : page_title,
        'OG_DESCRIPTION': settings.META_DESCRIPTION,
        #'OG_IMAGE': static('assets/jaribio_banner.png'),
        'OG_URL': request.build_absolute_uri(),
    }
    return render(request, template_name,context)


def about(request):
    """
    This function serves the About Page.
    By default the About html page is saved
    on the root template folder.
    """
    template_name = "about.html"
    page_title = 'About' + ' - ' + settings.SITE_NAME
    
    
    context = {
        'page_title': page_title,
    }
    return render(request, template_name,context)



def faq(request):
    template_name = "faq.html"
    page_title = "FAQ" + ' - ' + settings.SITE_NAME
    context = {
        'page_title': page_title,
    }
    return render(request, template_name,context)


def usage(request):
    template_name = "usage.html"
    page_title =  "Usage" + ' - ' + settings.SITE_NAME
    context = {
        'page_title': page_title
    }
    return render(request, template_name,context)


