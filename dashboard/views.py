from django.shortcuts import render, get_object_or_404, redirect
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.exceptions import PermissionDenied, SuspiciousOperation, ObjectDoesNotExist
from django.contrib.sessions.models import Session

from django.contrib.auth.models import User, Group, Permission
from django.http import Http404
from django.http import HttpRequest
from django.http import HttpResponseRedirect
from django.http import HttpResponseBadRequest
from django.http import HttpResponse
from django.urls import reverse, resolve
from django.http import HttpResponseRedirect, JsonResponse, HttpResponseForbidden
from django.contrib import messages
from django.db.models import F, Q, Count, Sum
from django.utils import timezone
from django.forms import formset_factory, modelformset_factory
from dashboard.permissions import PermissionManager, get_view_permissions
from dashboard import Constants
from dashboard.forms import AccountForm, GroupFormCreation, TokenForm
from dashboard.models import PartnerToken
from dashboard import dashboard_service
from rest_framework.authtoken.models import Token
from jaribio import utils, settings, conf as GLOBAL_CONF
from quiz.models import Category, Quiz, QuizStep,QuizSession, QuizImage, Question
from accounts import constants as Account_Constants
from accounts.forms import AccountCreationForm, UserCreationForm
from accounts import account_services

from core.tasks import send_mail_task
from core.resources import ui_strings as CORE_STRINGS

from itertools import islice
import json

import logging

logger = logging.getLogger(__name__)

# Create your views here.

#TODO : Add Required Login decoators

MAX_IMAGE_SIZE = 2097152


@login_required
def dashboard(request):
    template_name = "dashboard/dashboard.html"
    username = request.user.username
    can_view_dashboard = PermissionManager.user_can_access_dashboard(request.user)
    if not can_view_dashboard :
        logger.warning(f"Dashboard : PermissionDenied to user {username} for path {request.path}")
        raise PermissionDenied
    page_title = _('Dashboard') + ' - ' + settings.SITE_NAME
    now = timezone.now()

    recent_users = User.objects.all().order_by('-date_joined')[:Constants.MAX_RECENT]
    context = {
            'name'          : username,
            'page_title'    : page_title,
            'content_title' : CORE_STRINGS.DASHBOARD_DASHBOARD_TITLE,
            'is_allowed'     : can_view_dashboard,
            'users_count' : User.objects.count(),
            'user_list': recent_users,
        }
    context.update(get_view_permissions(request.user))

    logger.info(f"Authorized Access : User {username} has requested the Dashboard Page")

    return render(request, template_name, context)

@login_required
def category_create (request):
    template_name = 'dashboard/category_create.html'
    page_title = _('New Category')
    context = {
        'page_title': page_title,
        'content_title' : _('New Category')
    }
    username = request.user.username
    if not PermissionManager.user_can_access_dashboard(request.user):
        logger.warning("Dashboard : PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied

    if not PermissionManager.user_can_add_category(request.user):
        logger.warning("PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied
    

    return render(request,template_name, context)
    



@login_required
def categories(request):
    template_name = 'dashboard/category_list.html'
    page_title = _('Category List')
    context = {
        'page_title': page_title,
        'content_title' : _('Categories')
    }
    username = request.user.username
    if not PermissionManager.user_can_access_dashboard(request.user):
        logger.warning("Dashboard : PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied

    if not PermissionManager.user_can_view_category(request.user):
        logger.warning("PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied

    queryset = Category.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(queryset, GLOBAL_CONF.PAGINATED_BY)
    try:
        list_set = paginator.page(page)
    except PageNotAnInteger:
        list_set = paginator.page(1)
    except EmptyPage:
        list_set = None
    context['page_title'] = page_title
    context['category_list'] = list_set
    return render(request,template_name, context)

@login_required
def category_detail(request, category_uuid=None):
    template_name = 'dashboard/category_detail.html'
    page_title = _('Category')
    username = request.user.username
    if not PermissionManager.user_can_access_dashboard(request.user):
        logger.warning("Dashboard : PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied

    if not PermissionManager.user_can_view_category(request.user):
        logger.warning("PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied
    context = {
        'page_title': page_title
    }

    category = get_object_or_404(Category, category_uuid=category_uuid)
    
    context['page_title'] = page_title
    context['category'] = category
    context['content_title'] = category.display_name
    context['subcategory_list'] = Category.objects.filter(parent=category)

    return render(request,template_name, context)

@login_required
def category_update(request, category_uuid):
    template_name = 'dashboard/category_update.html'
    page_title = _('Edit Category')
    username = request.user.username
    if not PermissionManager.user_can_access_dashboard(request.user):
        logger.warning("Dashboard : PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied

    if not PermissionManager.user_can_change_category(request.user):
        logger.warning("PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied
    category = get_object_or_404(Category, category_uuid=category_uuid)
    
    context = {
        'page_title': page_title,
        'category':category,
        'category_list': Category.objects.exclude(id__in=[category.pk]),
        'content_title': f"{category.display_name} - {_('Update')}"
    }
    return render(request,template_name, context)

@login_required
def category_delete(request, category_uuid):
    username = request.user.username
    if not PermissionManager.user_can_access_dashboard(request.user):
        logger.warning("Dashboard : PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied

    if not PermissionManager.user_can_delete_category(request.user):
        logger.warning("PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied
    if request.method != "POST":
        raise SuspiciousOperation('Bad request. POST request expected but received a GET request')
    category = get_object_or_404(Category, category_uuid=category_uuid)
    Category.objects.filter(pk=category.pk).delete()
    return redirect('dashboard:categories')


@login_required
def categories_delete(request):
    username = request.user.username
    if not PermissionManager.user_can_access_dashboard(request.user):
        logger.warning("Dashboard : PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied

    if not PermissionManager.user_can_delete_category(request.user):
        logger.warning(f"PermissionDenied to user \"{username}\" for path \"{request.path}\"")
        raise PermissionDenied
    if request.method != "POST":
        raise SuspiciousOperation('Bad request')
    postdata = utils.get_postdata(request)
    id_list = postdata.getlist('categories')

    if len(id_list):
        category_list = list(map(int, id_list))
        Category.objects.filter(id__in=category_list).delete()
        messages.success(request, f"Catergories \"{category_list}\" deleted")
        logger.info(f"Categories \"{category_list}\" deleted by user {username}")
        
    else:
        messages.error(request, f"Catergories  could not be deleted")
        logger.error(f"ID list invalid. Error : {id_list}")
    return redirect('dashboard:categories')


@login_required
def category_manage_products(request, category_uuid):
    username = request.user.username
    if not PermissionManager.user_can_access_dashboard(request.user):
        logger.warning("Dashboard : PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied

    if not PermissionManager.user_can_change_category(request.user):
        logger.warning(f"PermissionDenied to user \"{username}\" for path \"{request.path}\"")
        raise PermissionDenied
    category = get_object_or_404(Category, category_uuid=category_uuid)
    template_name = 'dashboard/category_manage_products.html'
    page_title = _('Category Product Managements')
    
    context = {
        'category': category,
        'page_title' : page_title,
        'content_title' :_('Category Management')
    }
    
    
    return render(request,template_name, context)


@login_required
def category_products(request, category_uuid=None):
    template_name = 'dashboard/category_product_list.html'
    username = request.user.username
    
    if not PermissionManager.user_can_access_dashboard(request.user):
        logger.warning("Dashboard : PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied

    if not PermissionManager.user_can_view_category(request.user):
        logger.warning("PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied

    category = get_object_or_404(Category, category_uuid=category_uuid)
    page_title = _('Category')
    context = {
        'page_title': page_title,
        'category' : category
    }

    context['page_title'] = page_title

    return render(request,template_name, context)



@login_required
def add_products_highlight(request, highlight_uuid):
    username = request.user.username
    if not PermissionManager.user_can_access_dashboard(request.user):
        logger.warning("Dashboard : PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied

    if not PermissionManager.user_can_add_product(request.user):
        logger.warning("PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied

    form = None
    username = request.user.username
    #highlight = get_object_or_404(Highlight, highlight_uuid=highlight_uuid)
    if request.method == 'POST':
        postdata = utils.get_postdata(request)
        #form = AddAttributeForm(postdata)
        logger.info("Attribute formset valid checking")
        if form.is_valid():

            messages.success(request, _('formset valid'))
            logger.info(f'New attributes added by user \"{username}\"')
            logger.info(attributes)
        else:
            messages.error(request, _(' not added'))
            logger.error(f'Error on adding new. Action requested by user \"{username}\"')
            logger.error(form.errors)
            
    return render(request,"", {})


@login_required
def highlight_add_products(request, highlight_uuid):
    username = request.user.username
    if not PermissionManager.user_can_access_dashboard(request.user):
        logger.warning("Dashboard : PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied

    if not PermissionManager.user_can_delete_product(request.user):
        logger.warning("PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied

    if request.method != "POST":
        raise SuspiciousOperation('Bad request')

    #highlight = get_object_or_404(Highlight, highlight_uuid=highlight_uuid)
    postdata = utils.get_postdata(request)
    id_list = postdata.getlist('products')

    if len(id_list):
        id_list = list(map(int, id_list))
        #highlight.products.add(*id_list)
        #messages.success(request, f"Products \"{id_list}\" added to highlight {highlight.display_name}")
        #logger.info(f"Products \"{id_list}\" added to highlight {highlight.display_name} by user {username}")
        
    else:
        messages.error(request, f"ID list invalid. Error : {id_list}")
        logger.error(f"ID list invalid. Error : {id_list}")
    return redirect('dashboard:home')

@login_required
def highlights(request):
    username = request.user.username
    if not PermissionManager.user_can_access_dashboard(request.user):
        logger.warning("Dashboard : PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied

    if not PermissionManager.user_can_view_product(request.user):
        logger.warning("PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied

    template_name = 'dashboard/highlight_list.html'
    page_title = _('Highlights')
    context = {}

    context['page_title'] = page_title
    context['content_title'] = CORE_STRINGS.DASHBOARD_HIGHLIGHTS_TITLE
    return render(request,template_name, context)


@login_required
def highlight_create(request):
    template_name = 'dashboard/highlight_create.html'
    page_title = _('New Highlight')
    username = request.user.username
    if not PermissionManager.user_can_access_dashboard(request.user):
        logger.warning("Dashboard : PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied

    if not PermissionManager.user_can_add_product(request.user):
        logger.warning("PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied
    context = {
        'page_title': page_title,
    }
    form = None
    
    username = request.user.username
    if request.method == 'POST':
        postdata = utils.get_postdata(request)
        #form = HighlightForm(postdata)
        if form.is_valid():
            highlight = form.save()
            messages.success(request, _('New Highlight created'))
            logger.info(f'New highlight added by user \"{username}\"')
            return redirect(highlight.get_absolute_url())
        else:
            messages.error(request, _('Highlight not created'))
            logger.error(f'Error on creating new highlight. Action requested by user \"{username}\"')
            logger.error(form.errors.items())
    else:
        form = None
    context['form'] = form
    context['content_title'] = CORE_STRINGS.DASHBOARD_HIGHLIGHT_CREATE_TITLE
    context.update(get_view_permissions(request.user))
    return render(request, template_name, context)


@login_required
def highlight_detail(request, highlight_uuid=None):
    template_name = 'dashboard/highlight_detail.html'
    username = request.user.username
    if not PermissionManager.user_can_access_dashboard(request.user):
        logger.warning("Dashboard : PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied

    if not PermissionManager.user_can_view_product(request.user):
        logger.warning("PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied

    page_title = _('Highlight Detail')
    

    #highlight = get_object_or_404(Highlight, highlight_uuid=highlight_uuid)
    context = {
        'page_title': page_title,
        'content_title': CORE_STRINGS.DASHBOARD_HIGHLIGHT_TITLE
    }
    context.update(get_view_permissions(request.user))
    return render(request,template_name, context)


@login_required
def highlight_update(request, highlight_uuid=None):
    username = request.user.username
    if not PermissionManager.user_can_access_dashboard(request.user):
        logger.warning("Dashboard : PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied

    if not PermissionManager.user_can_change_product(request.user):
        logger.warning("PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied

    template_name = 'dashboard/highlight_update.html'
    page_title = _('Highlight Update')
    context = {
        'page_title': page_title,
    }
    form = None
   
    context['form'] = form

    context['content_title'] = CORE_STRINGS.DASHBOARD_HIGHLIGHT_UPDATE_TITLE
    return render(request, template_name, context)

@login_required
def highlight_delete(request, highlight_uuid=None):
    username = request.user.username
    if not PermissionManager.user_can_access_dashboard(request.user):
        logger.warning("Dashboard : PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied

    if not PermissionManager.user_can_delete_product(request.user):
        logger.warning("PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied

    if request.method != "POST":
        raise SuspiciousOperation('Bad request')

    messages.success(request, _('Highlight deleted'))
    return redirect('dashboard:highlights')


@login_required
def highlight_clear(request, highlight_uuid=None):
    username = request.user.username
    if not PermissionManager.user_can_access_dashboard(request.user):
        logger.warning("Dashboard : PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied

    if not PermissionManager.user_can_delete_product(request.user):
        logger.warning("PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied

    if request.method != "POST":
        raise SuspiciousOperation('Bad request')

    messages.success(request, _('Highlight deleted'))
    return redirect('dashboard:highlight-detail', highlight_uuid=highlight_uuid)


@login_required
def highlights_delete(request):
    username = request.user.username
    if not PermissionManager.user_can_access_dashboard(request.user):
        logger.warning("Dashboard : PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied

    if not PermissionManager.user_can_delete_product(request.user):
        logger.warning("PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied

    if request.method != "POST":
        raise SuspiciousOperation('Bad request')

    postdata = utils.get_postdata(request)
    id_list = postdata.getlist('highlights')

    if len(id_list):
        highlight_list = list(map(int, id_list))
        messages.success(request, f"Highlights \"{id_list}\" deleted")
        logger.info(f"Highlights \"{id_list}\" deleted by user {username}")
        
    else:
        messages.error(request, f"Highlight \"{id_list}\" could not be deleted")
        logger.error(f"ID list invalid. Error : {id_list}")
    return redirect('dashboard:highlights')


@login_required
def product_home(request):
    username = request.user.username
    if not PermissionManager.user_can_access_dashboard(request.user):
        logger.warning("Dashboard : PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied

    if not PermissionManager.user_can_view_product(request.user):
        logger.warning("PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied

    template_name = 'dashboard/product_home.html'
    page_title = _('Product')
    context = {
        'page_title': page_title,
    }
    
    context['page_title'] = page_title
    context['content_title'] = CORE_STRINGS.DASHBOARD_PRODUCT_HOME_TITLE
    context.update(Constants.DASHBOARD_PRODUCT_CONTEXT)
    return render(request,template_name, context)


@login_required
def products(request):
    username = request.user.username
    if not PermissionManager.user_can_access_dashboard(request.user):
        logger.warning("Dashboard : PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied

    if not PermissionManager.user_can_view_product(request.user):
        logger.warning("PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied

    template_name = 'dashboard/product_list.html'
    page_title = _('Products')
    context = {
        'page_title': page_title,
    }
    queryDict = request.GET.copy()
    
    context['page_title'] = page_title
    context['content_title'] = CORE_STRINGS.DASHBOARD_PRODUCTS_TITLE
    context.update(Constants.DASHBOARD_PRODUCT_CONTEXT)
    return render(request,template_name, context)

@login_required
def product_detail(request, product_uuid=None):
    template_name = 'dashboard/product_detail.html'
    username = request.user.username
    if not PermissionManager.user_can_access_dashboard(request.user):
        logger.warning("Dashboard : PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied

    if not PermissionManager.user_can_view_product(request.user):
        logger.warning("PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied

    page_title = _('Product Detail')
    
    context = {
        'page_title': page_title,

    }
    context.update(Constants.DASHBOARD_PRODUCT_CONTEXT)
    return render(request,template_name, context)

@login_required
def product_update(request, product_uuid=None):
    username = request.user.username
    if not PermissionManager.user_can_access_dashboard(request.user):
        logger.warning("Dashboard : PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied

    if not PermissionManager.user_can_change_product(request.user):
        logger.warning("PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied

    template_name = 'dashboard/product_update.html'
    page_title = _('Product Update')
    context = {
        'page_title': page_title,

    }
    form = None
   
    context['content_title'] = CORE_STRINGS.DASHBOARD_PRODUCT_UPDATE_TITLE
    context.update(Constants.DASHBOARD_PRODUCT_CONTEXT)
    return render(request, template_name, context)


@login_required
def products_changes(request):
    username = request.user.username
    if not PermissionManager.user_can_access_dashboard(request.user):
        logger.warning("Dashboard : PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied

    if not PermissionManager.user_can_change_product(request.user):
        logger.warning("PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied

    
    return redirect('dashboard:products')


@login_required
def product_toggle_active(request,product_uuid, toggle):
    username = request.user.username
    if not PermissionManager.user_can_access_dashboard(request.user):
        logger.warning("Dashboard : PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied

    if not PermissionManager.user_can_delete_product(request.user):
        logger.warning("PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied

    if request.method != "POST":
        logger.warn("product_toggle_active : only POST request required")
        raise SuspiciousOperation('Bad request')

    logger.info(f"product_toggle_active : toggle : {toggle} - type of toggle : {type(toggle)}")
    '''
    product = get_object_or_404(models.Product, product_uuid=product_uuid)
    p_name = product.name
    id_list, updated = inventory_service.products_toggle_active([product.pk], toggle)
    if updated:
        logger.info(f'Product \"{p_name}\" active status updated by user \"{request.user.username}\"')
        messages.success(request, _('Product updated'))
    '''
    return redirect('dashboard:products')




@login_required
def product_delete(request, product_uuid=None):
    username = request.user.username
    if not PermissionManager.user_can_access_dashboard(request.user):
        logger.warning("Dashboard : PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied

    if not PermissionManager.user_can_delete_product(request.user):
        logger.warning("PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied

    if request.method != "POST":
        logger.warn("product_delete : only POST request required")
        raise SuspiciousOperation('Bad request')

    messages.success(request, _('Product deleted'))
    return redirect('dashboard:products')


@login_required
def products_delete(request):
    username = request.user.username
    if not PermissionManager.user_can_access_dashboard(request.user):
        logger.warning("Dashboard : PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied

    if not PermissionManager.user_can_delete_product(request.user):
        logger.warning("PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied

    if request.method != "POST":
        logger.warn("product_delete : only POST request required")
        raise SuspiciousOperation('Bad request')

    postdata = utils.get_postdata(request)
    id_list = postdata.getlist('products')

    if len(id_list):
        product_id_list = list(map(int, id_list))
        messages.success(request, f"Products \"{id_list}\" deleted")
        logger.info(f"Products \"{id_list}\" deleted by user {username}")
        
    else:
        messages.error(request, f"Products \"{id_list}\" could not be deleted")
        logger.error(f"ID list invalid. Error : {id_list}")
    return redirect('dashboard:products')


@login_required
def product_image_create(request, product_uuid=None):
    username = request.user.username
    if not PermissionManager.user_can_access_dashboard(request.user):
        logger.warning("Dashboard : PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied

    if not PermissionManager.user_can_add_product(request.user):
        logger.warning("PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied
    context = {}    
    template_name = "dashboard/product_image_create.html"
    page_title = "New Product Image" + " - " + settings.SITE_NAME
    context['page_title'] = page_title
    forms_errors = []
    if request.method == "POST":
        files = request.FILES.copy()

        if forms_errors and len(forms_errors) and request.is_ajax():
                return JsonResponse({'status': 'NOT OK', 'message' : 'files not uploaded', 'errors' : forms_errors}, status=400)

        if request.is_ajax():
            return JsonResponse({'status': 'OK', 'message' : 'files uploaded'})
        return redirect('dashboard:product-detail', product_uuid=product_uuid)
        

    context['content_title'] = CORE_STRINGS.DASHBOARD_PRODUCT_IMAGE_CREATE_TITLE
    context.update(Constants.DASHBOARD_PRODUCT_CONTEXT)
    return render(request,template_name, context)

@login_required
def product_image_detail(request, image_uuid=None):
    username = request.user.username
    if not PermissionManager.user_can_access_dashboard(request.user):
        logger.warning("Dashboard : PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied

    if not PermissionManager.user_can_view_product(request.user):
        logger.warning("PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied

    context = {}

    template_name = "dashboard/product_image_detail.html"
    page_title = "Product Image" + " - " + settings.SITE_NAME
    context['page_title'] = page_title
    context['image'] = p_image
    context['content_title'] = CORE_STRINGS.DASHBOARD_PRODUCT_IMAGE_TITLE
    context.update(Constants.DASHBOARD_PRODUCT_CONTEXT)
    return render(request,template_name, context)


def product_image_delete(request, image_uuid=None):
    username = request.user.username
    if not PermissionManager.user_can_access_dashboard(request.user):
        logger.warning("Dashboard : PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied

    if not PermissionManager.user_can_delete_product(request.user):
        logger.warning("PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied
    
    if request.method != "POST":
        raise SuspiciousOperation('Bad request')

    context = {}

    p_image = get_object_or_404(QuizImage, image_uuid=image_uuid)
    
    return redirect('dashboard:home')

@login_required
def product_image_update(request, image_uuid=None):
    username = request.user.username
    if not PermissionManager.user_can_access_dashboard(request.user):
        logger.warning("Dashboard : PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied

    if not PermissionManager.user_can_change_product(request.user):
        logger.warning("PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied

    page_title = "Edit Product Image" + ' - ' + settings.SITE_NAME
    template_name = "dashboard/product_image_update.html"
    
    context = {
            'page_title': page_title,
            'template_name': template_name,
        }
    context['content_title'] = CORE_STRINGS.DASHBOARD_PRODUCT_IMAGE_UPDATE_TITLE
    context.update(Constants.DASHBOARD_PRODUCT_CONTEXT)
    return render(request, template_name,context )

@login_required
def product_images(request, product_uuid):
    username = request.user.username
    if not PermissionManager.user_can_access_dashboard(request.user):
        logger.warning("Dashboard : PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied

    if not PermissionManager.user_can_view_product(request.user):
        logger.warning("PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied

    context = {}
    
    template_name = "dashboard/product_images_list.html"
    page_title = "Product Images" + " - " + settings.SITE_NAME
    context['page_title'] = page_title
    context['content_title'] = f"Images" 
    return render(request,template_name, context)



@login_required
def tokens(request):
    username = request.user.username
    can_access_dashboard = PermissionManager.user_can_access_dashboard(request.user)
    if not can_access_dashboard:
        logger.warning("Dashboard : PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied
    can_view_user = PermissionManager.user_can_view_user(request.user)
    if not can_view_user:
        logger.warning("PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied

    context = {}
    queryset = Token.objects.all()
    template_name = "dashboard/token_list.html"
    page_title = _("Dashboard Users Tokens") + " - " + settings.SITE_NAME
    page = request.GET.get('page', 1)
    paginator = Paginator(queryset, GLOBAL_CONF.PAGINATED_BY)
    try:
        list_set = paginator.page(page)
    except PageNotAnInteger:
        list_set = paginator.page(1)
    except EmptyPage:
        list_set = None
    context['page_title'] = page_title
    context['token_list'] = list_set
    context['content_title'] =  CORE_STRINGS.DASHBOARD_TOKENS_TITLE
    context['can_delete'] = PermissionManager.user_can_delete_user(request.user)
    context.update(get_view_permissions(request.user))
    return render(request,template_name, context)

@login_required
def generate_token(request):
    username = request.user.username
    can_view_dashboard = PermissionManager.user_can_access_dashboard(request.user)
    if not can_view_dashboard :
        logger.warning("Dashboard : PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied
    can_generate_token = PermissionManager.user_can_generate_token(request.user)
    if not can_generate_token:
        logger.warning("PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied

    template_name = "dashboard/token_generate.html"
    context = {
        'page_title' :_('User Token Generation') + ' - ' + settings.SITE_NAME,
        'can_generate_token' : can_generate_token,
        'content_title' : CORE_STRINGS.DASHBOARD_TOKEN_CREATE_TITLE
    }
    if request.method == 'POST':
            form = TokenForm(utils.get_postdata(request))
            if form.is_valid():
                user_id = form.cleaned_data.get('user')
                user = User.objects.get(pk=user_id)
                t = Token.objects.get_or_create(user=user)
                context['generated_token'] = t
                logger.info("user \"%s\" create a token for user \"%s\"", request.user.username, user.username )
                messages.add_message(request, messages.SUCCESS, _(f'Token successfully generated for user {username}') )
                return redirect('dashboard:home')
            else :
                logger.error("TokenForm is invalid : %s\n%s", form.errors, form.non_field_errors)
                messages.add_message(request, messages.ERROR, _('The submitted form is not valid') )
    else :
            context['form'] = TokenForm()
            context.update(get_view_permissions(request.user))
        

    return render(request, template_name, context)



        
@login_required
def users(request):
    username = request.user.username
    can_access_dashboard = PermissionManager.user_can_access_dashboard(request.user)
    if not can_access_dashboard:
        logger.warning("Dashboard : PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied
    can_view_user = PermissionManager.user_can_view_user(request.user)
    if not can_view_user:
        logger.warning("PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied

    context = {}
    queryset = User.objects.order_by('-date_joined')
    template_name = "dashboard/user_list.html"
    page_title = _("Dashboard Users") + " - " + settings.SITE_NAME
    page = request.GET.get('page', 1)
    paginator = Paginator(queryset, GLOBAL_CONF.PAGINATED_BY)
    try:
        list_set = paginator.page(page)
    except PageNotAnInteger:
        list_set = paginator.page(1)
    except EmptyPage:
        list_set = None
    context['page_title'] = page_title
    context['users'] = list_set
    context['content_title'] = CORE_STRINGS.DASHBOARD_USERS_TITLE
    return render(request,template_name, context)

@login_required
def customers(request):
    username = request.user.username
    can_access_dashboard = PermissionManager.user_can_access_dashboard(request.user)
    if not can_access_dashboard:
        logger.warning("Dashboard : PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied
    can_view_user = PermissionManager.user_can_view_user(request.user)
    if not can_view_user:
        logger.warning("PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied

    context = {}
    template_name = "dashboard/customers.html"
    queryset = User.objects.order_by('-date_joined')
    page_title = _("Customers") + " - " + settings.SITE_NAME
    page = request.GET.get('page', 1)
    paginator = Paginator(queryset, GLOBAL_CONF.PAGINATED_BY)
    try:
        list_set = paginator.page(page)
    except PageNotAnInteger:
        list_set = paginator.page(1)
    except EmptyPage:
        list_set = None
    context['page_title'] = page_title
    context['customers'] = list_set
    context['content_title'] = CORE_STRINGS.DASHBOARD_CUSTOMERS_TITLE
    return render(request,template_name, context)



@login_required
def user_details(request, pk=None):
    username = request.user.username
    if not PermissionManager.user_can_access_dashboard(request.user):
        logger.warning("Dashboard : PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied
    if not PermissionManager.user_can_view_user(request.user):
        logger.warning("PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied
    context = {}
    #queryset = User.objects.select_related('account')
    user = get_object_or_404(User, pk=pk)
    seller_group = None
    template_name = "dashboard/user_detail.html"
    page_title = "User Details - " + settings.SITE_NAME
    context['page_title'] = page_title
    context['user_instance'] = user

    context['has_balance'] = hasattr(user, 'balance') and user.balance is not None
    context['ACCOUNT_TYPE'] = Account_Constants.ACCOUNT_TYPE
    context['content_title'] = f"{CORE_STRINGS.DASHBOARD_USER_TITLE} - {user.get_full_name()}"
    return render(request,template_name, context)






@login_required
def users_delete(request):
    username = request.user.username
    if not PermissionManager.user_can_access_dashboard(request.user):
        logger.warning("Dashboard : PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied

    if not PermissionManager.user_can_delete_user(request.user):
        logger.warning("PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied

    if request.method != "POST":
        raise SuspiciousOperation('Bad request. Expected POST request but received a GET')
    
    postdata = utils.get_postdata(request)
    id_list = postdata.getlist('users')

    if len(id_list):
        user_list = list(map(int, id_list))
        User.objects.filter(id__in=user_list).delete()
        messages.success(request, f"Users \"{id_list}\" deleted")
        logger.info(f"Users \"{id_list}\" deleted by user {username}")
        
    else:
        messages.error(request, f"Users \"\" could not be deleted")
        logger.error(f"ID list invalid. Error : {id_list}")
    return redirect('dashboard:users')

@login_required
def user_delete(request, pk=None):
    username = request.user.username
    if not PermissionManager.user_can_access_dashboard(request.user):
        logger.warning("Dashboard : PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied

    if not PermissionManager.user_can_delete_user(request.user):
        logger.warning("PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied

    if request.method != "POST":
        raise SuspiciousOperation('Bad request. Expected POST request but received a GET')
    
    postdata = utils.get_postdata(request)

    User.objects.filter(id=pk).delete()
    messages.success(request, f"Users \"{pk}\" deleted")
    logger.info(f"Users \"{pk}\" deleted by user {username}")
    return redirect('dashboard:users')


@login_required
def groups(request):
    username = request.user.username
    can_access_dashboard = PermissionManager.user_can_access_dashboard(request.user)
    if not can_access_dashboard:
        logger.warning("Dashboard : PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied

    can_view_group = PermissionManager.user_can_view_group(request.user)
    if not can_view_group:
        logger.warning("PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied

    context = {}
    
    #current_account = Account.objects.get(user=request.user)
    group_list = Group.objects.extra(select={'iname':'lower(name)'}).order_by('iname')
    template_name = "dashboard/group_list.html"
    page_title = "Groups" + " - " + settings.SITE_NAME
    page = request.GET.get('page', 1)
    paginator = Paginator(group_list, GLOBAL_CONF.PAGINATED_BY)
    try:
        group_set = paginator.page(page)
    except PageNotAnInteger:
        group_set = paginator.page(1)
    except EmptyPage:
        group_set = None
    context['page_title'] = page_title
    context['groups'] = group_set
    context['can_delete_group'] = PermissionManager.user_can_delete_group(request.user)
    context['can_update_group'] = PermissionManager.user_can_change_group(request.user)
    context['can_add_group'] = PermissionManager.user_can_add_group(request.user)
    context['content_title'] = CORE_STRINGS.DASHBOARD_GROUPS_TITLE

    return render(request,template_name, context)

@login_required
def group_detail(request, pk=None):
    username = request.user.username
    can_access_dashboard = PermissionManager.user_can_access_dashboard(request.user)
    if not can_access_dashboard:
        logger.warning("Dashboard : PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied

    can_view_group = PermissionManager.user_can_view_group(request.user)
    if not can_view_group:
        logger.warning("PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied

    context = {}
    group = get_object_or_404(Group, pk=pk)
    template_name = "dashboard/group_detail.html"
    page_title = "Group Detail" + " - " + settings.SITE_NAME
    context['page_title'] = page_title
    context['group'] = group
    context['can_delete_group'] = PermissionManager.user_can_delete_group(request.user)
    context['can_update_group'] = PermissionManager.user_can_change_group(request.user)
    context['content_title'] = CORE_STRINGS.DASHBOARD_GROUP_TITLE

    return render(request,template_name, context)


@login_required
def group_update(request, pk=None):
    # TODO CHECK if the requesting User has the permission to update a group
    username = request.user.username
    can_access_dashboard = PermissionManager.user_can_access_dashboard(request.user)
    if not can_access_dashboard:
        logger.warning("Dashboard : PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied

    can_change_group = PermissionManager.user_can_change_group(request.user)
    if not can_change_group:
        logger.warning("PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied

    context = None
    page_title = 'Group Update'
    template_name = 'dashboard/group_update.html'
    group = get_object_or_404(Group, pk=pk)
    form = GroupFormCreation(instance=group)
    group_users = group.user_set.all()
    available_users = User.objects.exclude(pk__in=group_users.values_list('pk'))
    permissions = group.permissions.all()
    available_permissions = Permission.objects.exclude(pk__in=permissions.values_list('pk'))
    if request.method == 'POST':
        form = GroupFormCreation(request.POST, instance=group)
        users = request.POST.getlist('users')
        if form.is_valid() :
            logger.debug("Group form for update is valid")
            if form.has_changed():
                logger.debug("Group has changed")
            group = form.save()
            if users:
                logger.debug("adding %s users [%s] into the group", len(users), users)
                group.user_set.set(users)
            logger.debug("Saved users into the group %s",users)
            return redirect('dashboard:groups')
        else :
            logger.error("Error on editing the group. The form is invalid")
    
    context = {
            'page_title' : page_title,
            'form': form,
            'group': group,
            'users' : group_users,
            'available_users' : available_users,
            'permissions': permissions,
            'available_permissions' : available_permissions,
            'can_change_group' : can_change_group,
            'content_title' : CORE_STRINGS.DASHBOARD_GROUP_UPDATE_TITLE
    }
    context.update(get_view_permissions(request.user))
    return render(request, template_name, context)


@login_required
def group_create(request):
    username = request.user.username
    can_access_dashboard = PermissionManager.user_can_access_dashboard(request.user)
    if not can_access_dashboard:
        logger.warning("Dashboard : PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied

    can_add_group = PermissionManager.user_can_add_group(request.user)
    if not can_add_group:
        logger.warning("PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied

    context = None
    page_title = 'Group Creation'
    template_name = 'dashboard/group_create.html'
    available_permissions = Permission.objects.all()
    available_users = User.objects.all()
    form = GroupFormCreation()
    if request.method == 'POST':
        form = GroupFormCreation(request.POST)
        users = request.POST.getlist('users')
        if form.is_valid():
            logger.debug("Group Create : Form is Valid")
            group_name = form.cleaned_data.get('name', None)
            logger.debug('Creating a Group with the name {}'.format(group_name))
            if not Group.objects.filter(name=group_name).exists():
                group = form.save()
                messages.success(request, "The Group has been succesfully created")
                if users:
                    group.user_set.set(users)
                    logger.debug("Added users into the group %s",users)
                else :
                    logger.debug("Group %s created without users", group_name)

                return redirect('dashboard:groups')
            else:
                msg = "A Group with the given name {} already exists".format(group_name)
                messages.error(request, msg)
                logger.error(msg)
            
        else :
            messages.error(request, "The Group could not be created. Please correct the form")
            logger.error("Error on creating new Group Errors : %s", form.errors)
    
    context = {
            'page_title' : page_title,
            'form': form,
            'available_users' : available_users,
            'available_permissions': available_permissions,
            'can_add_group' : can_add_group,
            'content_title' : CORE_STRINGS.DASHBOARD_GROUP_CREATE_TITLE
    }

    return render(request, template_name, context)


@login_required
def group_delete(request, pk=None):
    # TODO Check if the user requesting the deletion has the Group Delete permission
    username = request.user.username
    can_access_dashboard = PermissionManager.user_can_access_dashboard(request.user)
    if not can_access_dashboard:
        logger.warning("Dashboard : PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied

    can_delete_group = PermissionManager.user_can_delete_group(request.user)
    if not can_delete_group:
        logger.warning("PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied
    try:
        group = Group.objects.get(pk=pk)
        name = group.name
        messages.add_message(request, messages.SUCCESS, 'Group {} has been deleted'.format(name))
        group.delete()
        logger.debug("Group {} deleted by User {}", name, request.user.username)
        
    except Group.DoesNotExist:
        messages.add_message(request, messages.ERROR, 'Group could not be found. Group not deleted')
        logger.error("Group Delete : Group not found. Action requested by User {}",request.user.username)
        
    return redirect('dashboard:groups')


@login_required
def groups_delete(request):
    username = request.user.username
    if not PermissionManager.user_can_access_dashboard(request.user):
        logger.warning("Dashboard : PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied

    if not PermissionManager.user_can_delete_group(request.user):
        logger.warning("PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied

    if request.method != "POST":
        raise SuspiciousOperation('Bad request. Expected POST request but received a GET')
    
    postdata = utils.get_postdata(request)
    id_list = postdata.getlist('groups')

    if len(id_list):
        instance_list = list(map(int, id_list))
        Group.objects.filter(id__in=instance_list).delete()
        messages.success(request, f"Groups \"{instance_list}\" deleted")
        logger.info(f"Groups \"{instance_list}\" deleted by user {username}")
        
    else:
        messages.error(request, f"Groups could not be deleted")
        logger.error(f"ID list invalid. Error : {id_list}")
    return redirect('dashboard:groups')


#######################################################
########            Permissions 

@login_required
def permissions(request):
    username = request.user.username
    can_access_dashboard = PermissionManager.user_can_access_dashboard(request.user)
    if not can_access_dashboard:
        logger.warning("Dashboard : PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied


    context = {}
    permission_list = Permission.objects.all()
    template_name = "dashboard/permission_list.html"
    page_title = "Permissions" + " - " + settings.SITE_NAME
    page = request.GET.get('page', 1)
    paginator = Paginator(permission_list, GLOBAL_CONF.PAGINATED_BY)
    try:
        permission_set = paginator.page(page)
    except PageNotAnInteger:
        permission_set = paginator.page(1)
    except EmptyPage:
        permission_set = None
    context['page_title'] = page_title
    context['permissions'] = permission_set

    return render(request,template_name, context)

@login_required
def permission_detail(request, pk=None):
    username = request.user.username
    can_access_dashboard = PermissionManager.user_can_access_dashboard(request.user)
    if not can_access_dashboard:
        logger.warning("Dashboard : PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied

    context = {}
    permission = get_object_or_404(Permission, pk=pk)
    template_name = "dashboard/permission_detail.html"
    page_title = "Permission Detail" + " - " + settings.SITE_NAME
    context['page_title'] = page_title
    context['permission'] = permission

    return render(request,template_name, context)


@login_required
def permission_update(request, pk=None):
    # TODO CHECK if the requesting User has the permission to update a permission
    username = request.user.username
    can_access_dashboard = PermissionManager.user_can_access_dashboard(request.user)
    if not can_access_dashboard:
        logger.warning("Dashboard : PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied

    context = None
    page_title = 'Permission Update'
    template_name = 'dashboard/permission_update.html'
    permission = get_object_or_404(Permission, pk=pk)
    form = GroupFormCreation(instance=permission)
    permission_users = permission.user_set.all()
    available_users = User.objects.exclude(pk__in=permission_users.values_list('pk'))

    if request.method == 'POST':
        form = GroupFormCreation(request.POST, instance=permission)
        users = request.POST.getlist('users')
        if form.is_valid() :
            logger.debug("Permission form for update is valid")
            if form.has_changed():
                logger.debug("Permission has changed")
            permission = form.save()
            if users:
                logger.debug("adding %s users [%s] into the permission", len(users), users)
                permission.user_set.set(users)
            logger.debug("Added permissions to users %s",users)
            return redirect('dashboard:permissions')
        else :
            logger.error("Error on editing the perssion. The form is invalid")
    
    context = {
            'page_title' : page_title,
            'form': form,
            'users' : permission_users,
            'available_users' : available_users,
            'permission': permission
    }

    return render(request, template_name, context)


@login_required
def permission_create(request):
    username = request.user.username
    can_access_dashboard = PermissionManager.user_can_access_dashboard(request.user)
    if not can_access_dashboard:
        logger.warning("Dashboard : PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied

    context = None
    page_title = 'Permission Creation'
    template_name = 'dashboard/permission_create.html'
    available_groups = Group.objects.all()
    available_users = User.objects.all()
    form = GroupFormCreation()
    if request.method == 'POST':
        form = GroupFormCreation(request.POST)
        users = request.POST.getlist('users')
        if form.is_valid():
            logger.debug("Permission Create : Form is Valid")
            perm_name = form.cleaned_data.get('name', None)
            perm_codename = form.cleaned_data.get('codename', None)
            logger.debug('Creating a Permission with the name {}'.format(perm_name))
            if not Permission.objects.filter(Q(name=perm_name) | Q(codename=perm_codename)).exists():
                perm = form.save()
                messages.add_message(request, messages.SUCCESS, "The Permission has been succesfully created")
                if users:
                    perm.user_set.set(users)
                    logger.debug("Permission %s given to users  %s",perm_name, users)
                else :
                    logger.debug("Permission %s created without users", perm_name)

                return redirect('dashboard:permissions')
            else:
                msg = "A Permission with the given name {} already exists".format(perm_name)
                messages.add_message(request, messages.ERROR, msg)
                logger.error(msg)
            
        else :
            messages.add_message(request, messages.ERROR, "The Permission could not be created. Please correct the form")
            logger.error("Error on creating new Permission : %s", form.errors)
    
    context = {
            'page_title' : page_title,
            'form': form,
            'available_users' : available_users,
            'available_groups': available_groups
    }

    return render(request, template_name, context)


@login_required
def permission_delete(request, pk=None):
    # TODO Check if the user requesting the deletion has the Group Delete permission
    username = request.user.username
    can_access_dashboard = PermissionManager.user_can_access_dashboard(request.user)
    if not can_access_dashboard:
        logger.warning("Dashboard : PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied

    try:
        perm = Permission.objects.get(pk=pk)
        name = perm.name
        messages.add_message(request, messages.SUCCESS, 'Permission {} has been deleted'.format(name))
        perm.delete()
        logger.debug("Permission {} deleted by User {}", name, request.user.username)
        
    except Permission.DoesNotExist:
        messages.add_message(request, messages.ERROR, 'Permission could not be found. Permission not deleted')
        logger.error("Permission Delete : Permission not found. Action requested by User {}",request.user.username)
        raise Http404('Permission does not exist')
        
    return redirect('dashboard:permissions')


@login_required
def create_account(request):
    username = request.user.username
    context = {
        'page_title':_('New User') + ' - ' + settings.SITE_NAME,
        'ACCOUNT_TYPE' : Account_Constants.ACCOUNT_TYPE,
    }
    template_name = 'dashboard/new_user.html'
    can_access_dashboard = PermissionManager.user_can_access_dashboard(request.user)
    if not can_access_dashboard:
        logger.warning("Dashboard : PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied
    can_view_user = PermissionManager.user_can_view_user(request.user)
    can_add_user = PermissionManager.user_can_add_user(request.user)
    if not (can_add_user and can_view_user):
        logger.warning("PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied
    if request.method == 'POST':
        name = request.POST['username']
        result =account_services.AccountService.process_registration_request(request)
        if result['user_created']:
            messages.success(request, _(f"User {name} created"))
            return redirect('dashboard:users')
        else:
            user_form = UserCreationForm(request.POST)
            account_form = AccountCreationForm(request.POST)
            user_form.is_valid()
            account_form.is_valid()
    else:
        user_form = UserCreationForm()
        account_form = AccountCreationForm()
    context.update(get_view_permissions(request.user))
    context['can_add_user'] = can_add_user
    context['user_form'] = user_form
    context['account_form'] = account_form
    context['content_title'] = CORE_STRINGS.DASHBOARD_USER_CREATE_TITLE
    return render(request, template_name, context)


@login_required
def send_welcome_mail(request, pk):
    username = request.user.username
    if not PermissionManager.user_can_access_dashboard(request.user):
        logger.warning("Dashboard : PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied
    user = get_object_or_404(User, pk=pk)
    email_context = {
            'template_name': settings.DJANGO_WELCOME_EMAIL_TEMPLATE,
            'title': 'Bienvenu chez ' + settings.SITE_NAME,
            'recipient_email': user.email,
            'context':{
                'SITE_NAME': settings.SITE_NAME,
                'SITE_HOST': settings.SITE_HOST,
                'FULL_NAME': user.get_full_name()
            }
    }
    logger.info(f"Sending Welcome mail to user {user.username}")
    send_mail_task.apply_async(
        args=[email_context],
        queue=settings.CELERY_OUTGOING_MAIL_QUEUE,
        routing_key=settings.CELERY_OUTGOING_MAIL_ROUTING_KEY
    )
    logger.info(f"sent Welcome mail to user {user.username}")
    return redirect('dashboard:user-detail', pk=pk)




@login_required
def partner_tokens(request):
    username = request.user.username
    can_access_dashboard = PermissionManager.user_can_access_dashboard(request.user)
    if not can_access_dashboard:
        logger.warning("Dashboard : PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied
    can_view_user = PermissionManager.user_can_view_user(request.user)
    if not can_view_user:
        logger.warning("PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied

    context = {}
    queryset = PartnerToken.objects.all()
    template_name = "dashboard/partner_token_list.html"
    page_title = _("Dashboard Partner Tokens") + " - " + settings.SITE_NAME
    page = request.GET.get('page', 1)
    paginator = Paginator(queryset, GLOBAL_CONF.PAGINATED_BY)
    try:
        list_set = paginator.page(page)
        context.update(utils.prepare_pagination(paginator.num_pages, int(page)))
    except PageNotAnInteger:
        list_set = paginator.page(1)
    except EmptyPage:
        list_set = None
    context['page_title'] = page_title
    context['token_list'] = list_set
    context['content_title'] = CORE_STRINGS.DASHBOARD_PARTNER_TOKENS_TITLE
    return render(request,template_name, context)


@login_required
def create_partner_token(request):
    username = request.user.username
    if not PermissionManager.user_can_access_dashboard(request.user):
        logger.warning("Dashboard : PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied
    template_name = 'dashboard/partner_token_create.html'
    page_title = _("Partner Token")
    if request.method == 'POST':
        p_token = dashboard_service.create_partner_token(utils.get_postdata(request))
        if p_token:
            messages.add_message(request, messages.SUCCESS, message=_('Partner Token created'))
            return redirect(p_token.get_dashboard_url())
        else:
            messages.add_message(request, messages.ERROR, message=_('Partner Token not created'))
    context = {
        'page_title' : page_title,
        'content_title': page_title,
        'partner_list': User.objects.filter(groups__name=GLOBAL_CONF.PARTNER_GROUP)
    }
    return render(request, template_name, context)


@login_required
def update_partner_token(request, token_uuid):
    username = request.user.username
    if not PermissionManager.user_can_access_dashboard(request.user):
        logger.warning("Dashboard : PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied
    template_name = 'dashboard/partner_token_update.html'
    page_title = _("Partner Token")
    p_token = get_object_or_404(PartnerToken, token_uuid=token_uuid)
    if request.method == 'POST':
        p_token, updated = dashboard_service.update_partner_token(p_token, utils.get_postdata(request))
        if updated:
            messages.add_message(request, messages.SUCCESS, message=_('Partner Token update'))
            return redirect(p_token.get_dashboard_url())
        else:
            messages.add_message(request, messages.ERROR, message=_('Partner Token not updated'))
    context = {
        'page_title' : page_title,
        'p_token': p_token
    }
    return render(request, template_name, context)

@login_required
def partner_token_details(request, token_uuid):
    username = request.user.username
    if not PermissionManager.user_can_access_dashboard(request.user):
        logger.warning("Dashboard : PermissionDenied to user %s for path %s", username, request.path)
        raise PermissionDenied
    template_name = 'dashboard/partner_token_details.html'
    page_title = _("Partner Token")
    p_token = get_object_or_404(PartnerToken, token_uuid=token_uuid)
    context = {
        'page_title' : page_title,
        'p_token': p_token
    }
    return render(request, template_name, context)





