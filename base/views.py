from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import AddSiteSerializer, ClientSerializer, NoteSerializer, AddNoteSerializer, UpdateSiteSerializer
from .models import User, Client, Site, ExternalLinksManager, ExternalLink, Note
from .utils.find_external_links import get_external_links, get_pages_from_sitemap
from .utils.check_site_availability import is_site_available
from .utils.utils import get_domain_from_url
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
def site_details(request, site_id=None):  
    site = Site.objects.get(id=site_id)

    site.payment_date = site.payment_date.strftime('%Y-%m-%d')       
    return render(request, 'base/site-details.html', context={
        'site': site,
    })


@api_view(['GET', 'POST'])
def add_site(request):
    if request.method == 'GET':
        clients = Client.objects.all()
        return render(request, 'base/add-site.html', context={
            'clients': clients,
        })
    
    elif request.method == 'POST':
        serializer = AddSiteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Successfully added site'}, 200)
        return Response({'message': 'Submitted data is incorrect.'}, 400)


@api_view(['PUT'])
def edit_site(request):
    site_id = request.data.get('site_id')
    site = get_object_or_404(Site, id=site_id)
    serializer = UpdateSiteSerializer(site, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Successfully edited site'}, 200)
    return Response({'message': 'Submitted data is incorrect.'}, 400)
    

@api_view(['POST'])
def add_client(request):
    serializer = ClientSerializer(data=request.data)
    if serializer.is_valid():
        client = Client(
            name=serializer.validated_data['name'],
            nip=serializer.validated_data['nip'],
            email=serializer.validated_data['email'],
        )
        client.save()

        return Response({
            'client_id': client.id,
        }, 200)
    return Response('Submitted data is incorrect.', 400)


@api_view(['GET'])
def get_sites(request, site_id=None):
    if site_id:
        return Response(Site.objects.get(id=site_id).as_json(), 200)
    
    sites = Site.objects.all()
    new_sites = []
    for site in sites:
        new_sites.append(site.as_json())
            
    return Response(new_sites, 200)


@api_view(['PUT'])
def set_current_site(request):
    site_id = request.data.get('site_id')
    _ = get_object_or_404(Site, id=site_id)
    request.session['current_site'] = site_id
    return Response('Successfully setted current site', 200)


''' ============ external links views ============ '''

@site_required
def external_links(request, site_id=None):
    site = get_object_or_404(Site, id=site_id)
    external_links_manager = get_object_or_none(ExternalLinksManager, site=site)

    return render(request, 'base/external-links.html', context={
        'external_links': external_links_manager,
        'site_id': site_id,
    })


@api_view(['PUT'])
def check_linked_pages_availability(request):
    external_links_id = request.data.get('external_links_id')
    external_links_manager = get_object_or_404(ExternalLinksManager, id=external_links_id)

    #get rid of the same urls
    unique_linked_pages = set()
    for external_link in external_links_manager.links.all():
        unique_linked_pages.add(external_link.linked_page)

    #prepare external_links_manager progress
    external_links_manager.progress_target = len(unique_linked_pages)
    external_links_manager.progress_current = 0
    external_links_manager.save()

    #check availability for every unique linked page
    for linked_page in unique_linked_pages:
        is_available = is_site_available(linked_page)

        #update every ExternalLink object with checked URL
        objects_to_update = external_links_manager.links.filter(linked_page=linked_page)
        for object_to_update in objects_to_update:
            object_to_update.is_linked_page_available = is_available
            object_to_update.save()
        
        external_links_manager.progress_current += 1
        external_links_manager.save()
    
    #clear progress
    external_links_manager.progress_current = 0
    external_links_manager.save()

    return Response({'message': 'Successfully checked linked pages availability'}, 200)


@api_view(['PUT'])
def find_external_links(request):
    site = get_object_or_404(Site, id=request.data.get('site_id'))
    external_links_manager, _ = ExternalLinksManager.objects.get_or_create(site=site)
    pages = get_pages_from_sitemap(site.url)
    to_exclude = request.data.get('to_exclude')

    #prepare external_links_manager
    external_links_manager.progress_current = 0
    external_links_manager.progress_target = len(pages)
    external_links_manager.excluded = to_exclude
    external_links_manager.links.all().delete()
    external_links_manager.save()

    #iterates over all pages in site
    for page in pages:
        links = get_external_links(page, to_exclude)

        #iterates over all links in page, creates ExternalLink object and adds it to ExternalLinksManager
        for link in links:
            external_link_object = ExternalLink(
                linking_page=page,
                linked_page=link['href'],
                rel=link['rel'],
            )
            external_link_object.save()
            external_links_manager.links.add(external_link_object)
        external_links_manager.progress_current += 1
        external_links_manager.save()

    #clear progress
    external_links_manager.progress_current = 0
    external_links_manager.save()

    return Response({'message': 'Successfully found links'}, status=200)


@api_view(['GET'])
def get_external_links_progress(request, pk):
    site = get_object_or_404(Site, id=pk)
    external_links_manager = ExternalLinksManager.objects.get(site=site)
        
    return Response({
        'current': external_links_manager.progress_current,
        'target': external_links_manager.progress_target,
    }, 200)


''' ============ notes views ============ '''

@site_required
def notes(request, site_id=None):
    site = get_object_or_404(Site, id=site_id)
    notes = Note.objects.filter(site=site)
    
    return render(request, 'base/notes.html', context={
        'notes': notes,
        'site_id': site_id
    })


@api_view(['POST'])
def add_note(request):
    serializer = AddNoteSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, 201)
    return Response(serializer.errors, 400)


@api_view(['GET'])
def get_note(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    return Response(note.as_json(), 200)


@api_view(['PUT'])
def update_note(request):
    note_id = request.data.get('note_id')
    note = get_object_or_404(Note, id=note_id)
    serializer = NoteSerializer(note, data=request.data)
    
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Note updated successfully'}, 200)
    
    return Response(serializer.errors, 400)


@api_view(['DELETE'])
def delete_note(request):
    note_id = request.data.get('note_id')
    note = get_object_or_404(Note, id=note_id)
    note.delete()
    return Response({'message': 'Note deleted successfully'}, 200)
    

def site_choice(request):
    return render(request, 'base/site-choice.html')