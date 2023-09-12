from .serializers import AddSiteSerializer, ClientSerializer, NoteSerializer, AddNoteSerializer, UpdateSiteSerializer, LoginSerializer, AddBacklinkSerializer
from .utils import get_external_links, get_pages_from_sitemap, is_site_available
from ..models import Site, ExternalLinksManager, ExternalLink, Note, Backlink
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login, logout
from rest_framework.permissions import IsAuthenticated, BasePermission
from crm.settings import ALLOWED_USERS

class IsAllowedUser(BasePermission):

    def has_permission(self, request, view):
        return request.user.username in ALLOWED_USERS


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAllowedUser])
def add_site(request):
    serializer = AddSiteSerializer(data=request.data)
    
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Successfully added site'}, 200)
    return Response({'message': 'Submitted data is incorrect.'}, 400)


@api_view(['PUT'])
@permission_classes([IsAuthenticated, IsAllowedUser])
def edit_site(request):
    site_id = request.data.get('site_id')
    site = get_object_or_404(Site, id=site_id)
    serializer = UpdateSiteSerializer(site, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Successfully edited site'}, 200)
    return Response({'message': 'Submitted data is incorrect.'}, 400)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated, IsAllowedUser])
def delete_site(request):
    site_id = int(request.data.get('site_id'))
    site = get_object_or_404(Site, id=site_id)

    if site_id == request.session['current_site']:
        del request.session['current_site']
    site.delete()
    return Response({'message': 'Successfully deleted site'}, 200)


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAllowedUser])
def add_client(request):
    serializer = ClientSerializer(data=request.data)

    if serializer.is_valid():
        client = serializer.save()
        return Response({'client_id': client.id}, 200)
    return Response('Submitted data is incorrect.', 400)


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAllowedUser])
def get_sites(request, site_id=None):
    if site_id:
        return Response(Site.objects.get(id=site_id).as_json(), 200)
    
    sites = Site.objects.all()
    new_sites = []
    for site in sites:
        new_sites.append(site.as_json())
            
    return Response(new_sites, 200)


@api_view(['PUT'])
@permission_classes([IsAuthenticated, IsAllowedUser])
def set_current_site(request):
    site_id = request.data.get('site_id')
    _ = get_object_or_404(Site, id=site_id)
    request.session['current_site'] = site_id
    return Response('Successfully setted current site', 200)


@api_view(['PUT'])
@permission_classes([IsAuthenticated, IsAllowedUser])
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
@permission_classes([IsAuthenticated, IsAllowedUser])
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
@permission_classes([IsAuthenticated, IsAllowedUser])
def get_external_links_progress(request, pk):
    site = get_object_or_404(Site, id=pk)
    external_links_manager = ExternalLinksManager.objects.get(site=site)
        
    return Response({
        'current': external_links_manager.progress_current,
        'target': external_links_manager.progress_target,
    }, 200)


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAllowedUser])
def add_note(request):
    serializer = AddNoteSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Added backlink'}, 201)
    return Response(serializer.errors, 400)


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAllowedUser])
def get_note(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    return Response(note.as_json(), 200)


@api_view(['PUT'])
@permission_classes([IsAuthenticated, IsAllowedUser])
def update_note(request):
    note_id = request.data.get('note_id')
    note = get_object_or_404(Note, id=note_id)
    serializer = NoteSerializer(note, data=request.data)
    
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Note updated successfully'}, 200)
    
    return Response(serializer.errors, 400)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated, IsAllowedUser])
def delete_note(request):
    note_id = request.data.get('note_id')
    note = get_object_or_404(Note, id=note_id)
    note.delete()
    return Response({'message': 'Note deleted successfully'}, 200)
    

@api_view(['POST'])
def login_view(request):
    serializer = LoginSerializer(data=request.data)
    if not serializer.is_valid():
        return Response({'message': 'Submitted data is not valid'}, 400)
    
    user = authenticate(
        request._request, 
        username=serializer.validated_data['username'], 
        password=serializer.validated_data['password'],
    )

    if user is not None:
        login(request._request, user)
        return Response({'message': 'Successfully logged in'}, 200)
    else:
        return Response({'message': 'Incorrect username or password'}, 400)
    

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    logout(request._request)
    return Response({'message': 'Successfully logged out'}, 200)


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAllowedUser])
def add_backlink(request):
    serializer = AddBacklinkSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Added backlink'}, 201)
    return Response(serializer.errors, 400)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated, IsAllowedUser])
def delete_backlink(request):
    backlink_id = request.data.get('backlink_id')
    backlink = get_object_or_404(Backlink, id=backlink_id)
    backlink.delete()
    return Response({'message': 'Deleted backlink'}, 200)


@api_view(['PUT'])
@permission_classes([IsAuthenticated, IsAllowedUser])
def check_backlinks_status(request):
    site_id = request.data.get('site_id')
    site = get_object_or_404(Site, id=site_id)
    backlinks = site.backlinks

    for backlink in backlinks.all():
        linking_page = link.linking_page
        links_from_linking_page = get_external_links(linking_page)

        is_active, rel = False, None
        for link in links_from_linking_page:
            if site.url in link['href']:
                is_active = True
                rel = link['rel']
        
        backlink.active = is_active
        backlink.rel = rel
        backlink.save()
    
    return Response({'message': 'Updated backlinks statuses'}, 200)
