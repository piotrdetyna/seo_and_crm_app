from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import User, Client, Site, ExternalLinksManager, ExternalLink, Note
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect

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


def get_object_or_none(model, **kwargs):
    try:
        return model.objects.get(**kwargs)
    except ObjectDoesNotExist:
        return None


def index(request):
    return render(request, 'base/index.html')


@site_required
def notes(request, site_id=None):
    site = get_object_or_404(Site, id=site_id)
    notes = Note.objects.filter(site=site)
    
    return render(request, 'base/notes.html', context={
        'notes': notes,
        'site_id': site_id
    })


@site_required
def external_links(request, site_id=None):
    site = get_object_or_404(Site, id=site_id)
    external_links_manager = get_object_or_none(ExternalLinksManager, site=site)

    return render(request, 'base/external-links.html', context={
        'external_links': external_links_manager,
        'site_id': site_id,
    })


@site_required
def site_details(request, site_id=None):  
    site = Site.objects.get(id=site_id)
    site.payment_date = site.payment_date.strftime('%Y-%m-%d')     

    return render(request, 'base/site-details.html', context={
        'site': site,
    })


def site_choice(request):
    return render(request, 'base/site-choice.html')


def add_site_form(request):
    clients = Client.objects.all()

    return render(request, 'base/add-site.html', context={
        'clients': clients,
    })