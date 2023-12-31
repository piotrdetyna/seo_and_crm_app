from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Keyword, Client, Site, ExternalLinksManager, Invoice, Note, Contract, Backlink, ExternalLink
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from crm.settings import ALLOWED_USERS


def site_required(view_func):
    def _wrapped_view_func(request, *args, **kwargs):
        site_id = kwargs.pop('site_id', None)
        
        if not site_id:
            site_id = request.session.get('current_site', None)
        
        if site_id:
            return view_func(request, site_id, *args, **kwargs)
        else:
            original_url = request.get_full_path()
            url = f"/site-choice/?next={original_url}"
            return HttpResponseRedirect(url)
    
    return _wrapped_view_func


def is_allowed_user(user):
    return user.username in ALLOWED_USERS


def get_object_or_none(model, **kwargs):
    try:
        return model.objects.get(**kwargs)
    except ObjectDoesNotExist:
        return None
    

def login(request):
    return render(request, 'base/login.html')


@login_required
@user_passes_test(is_allowed_user)
def index(request):
    urgent_contracts = Contract.objects.filter(is_urgent=True)
    not_paid_invoices = Invoice.objects.filter(is_paid=False)
    not_active_backlinks = Backlink.objects.filter(active=False)
    broken_external_links = ExternalLink.objects.filter(is_linked_page_available=False)

    return render(request, 'base/index.html', {
        'urgent_contracts': urgent_contracts,
        'not_paid_invoices': not_paid_invoices,
        'not_active_backlinks': not_active_backlinks,
        'broken_external_links': broken_external_links,
    })


@login_required
@user_passes_test(is_allowed_user)
@site_required
def notes(request, site_id=None):
    site = get_object_or_404(Site, id=site_id)
    notes = Note.objects.filter(site=site)
    
    return render(request, 'base/notes.html', context={
        'notes': notes,
        'site': site
    })

@login_required
@user_passes_test(is_allowed_user)
@site_required
def external_links(request, site_id=None):
    site = get_object_or_404(Site, id=site_id)
    external_links_manager = get_object_or_none(ExternalLinksManager, site=site)

    return render(request, 'base/external-links.html', context={
        'external_links_manager': external_links_manager,
        'site': site,
    })


@login_required
@user_passes_test(is_allowed_user)
@site_required
def site_details(request, site_id=None):  
    site = Site.objects.get(id=site_id)

    return render(request, 'base/site-details.html', context={
        'site': site,
    })


@login_required
@user_passes_test(is_allowed_user)
def clients(request):  
    clients = Client.objects.all()

    return render(request, 'base/clients.html', context={
        'clients': clients,
    })


@login_required
@user_passes_test(is_allowed_user)
def client(request, client_id):  
    client = get_object_or_404(Client, id=client_id)

    return render(request, 'base/client.html', context={
        'client': client,
    })


@login_required
@user_passes_test(is_allowed_user)
def contracts(request):  
    contracts = Contract.objects.all()
    sites = Site.objects.all()

    return render(request, 'base/contracts.html', context={
        'contracts': contracts,
        'sites': sites,
        'categories': Contract.CATEGORIES,
    })


@login_required
@user_passes_test(is_allowed_user)
def contract(request, contract_id):  
    contract = get_object_or_404(Contract, id=contract_id)
    sites = Site.objects.all()
    return render(request, 'base/contract.html', context={
        'contract': contract,
        'sites': sites,
        'categories': Contract.CATEGORIES,
    })


@login_required
@user_passes_test(is_allowed_user)
def site_choice(request):
    return render(request, 'base/site-choice.html')


@login_required
@user_passes_test(is_allowed_user)
def add_site_form(request):
    clients = Client.objects.all()

    return render(request, 'base/add-site.html', context={
        'clients': clients,
    })


@login_required
@user_passes_test(is_allowed_user)
@site_required
def backlinks(request, site_id):
    site = get_object_or_404(Site, id=site_id) 
    return render(request, 'base/backlinks.html', context={
        'site': site,
        'backlinks': site.backlinks,
    })

@login_required
@user_passes_test(is_allowed_user)
@site_required
def keywords(request, site_id):  
    site = get_object_or_404(Site, id=site_id)
    keywords = site.keywords.all()

    return render(request, 'base/keywords.html', context={
        'keywords': keywords,
        'site': site,
    })


@login_required
@user_passes_test(is_allowed_user)
def invoices(request, contract_id=None):
    
    if contract_id:
        contract = get_object_or_404(Contract, id=contract_id) 
        invoices = contract.invoices.all()
        contracts = contract
        single_contract = True
    else:
        invoices = Invoice.objects.all()
        contracts = Contract.objects.all()
        single_contract = False
    
    return render(request, 'base/invoices.html', context={
        'invoices': invoices,
        'contracts': contracts,
        'single_contract': single_contract,
    })

@login_required
@user_passes_test(is_allowed_user)
def invoice(request, invoice_id):  
    invoice = get_object_or_404(Invoice, id=invoice_id)

    return render(request, 'base/invoice.html', context={
        'invoice': invoice,
    })


@login_required
@user_passes_test(is_allowed_user)
def sites(request):  
    sites = Site.objects.all()

    return render(request, 'base/sites.html', context={
        'sites': sites,
    })





