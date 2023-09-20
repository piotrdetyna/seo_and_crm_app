from .serializers import AddSiteSerializer, BacklinkSerializer, ContractSerializer, InvoiceSerializer, UpdateNoteSerializer, ClientSerializer, SiteSerializer, NoteSerializer, AddNoteSerializer, UpdateSiteSerializer, LoginSerializer, AddBacklinkSerializer, ExternalLinksManagerSerializer
from .utils import get_external_links, get_pages_from_sitemap, is_site_available, get_company_info
from ..models import Site, ExternalLinksManager, ExternalLink, Note, Backlink, Client, Contract, Invoice
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login, logout
from rest_framework.permissions import IsAuthenticated, BasePermission
from crm.settings import ALLOWED_USERS
from datetime import date, timedelta


class IsAllowedUser(BasePermission):

    def has_permission(self, request, view):
        return request.user.username in ALLOWED_USERS


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAllowedUser])
def add_site(request):
    serializer = AddSiteSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response({
            'message': 'Successfully added site', 
            'site': serializer.data,
        }, 201)
    return Response({'message': 'Submitted data is incorrect.'}, 400)


@api_view(['PUT'])
@permission_classes([IsAuthenticated, IsAllowedUser])
def edit_site(request, site_id):
    site = get_object_or_404(Site, id=site_id)
    serializer = UpdateSiteSerializer(site, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response({
            'message': 'Successfully edited site', 
            'site': serializer.data,           
            }, 200)
    return Response({'message': 'Submitted data is incorrect.'}, 400)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated, IsAllowedUser])
def delete_site(request, site_id):
    site = get_object_or_404(Site, id=site_id)

    if site_id == request.session['current_site']:
        del request.session['current_site']
    site.delete()
    return Response(status=204)


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAllowedUser])
def get_sites(request, site_id=None):
    if site_id:
        site = SiteSerializer(Site.objects.get(id=site_id)).data
        return Response({'site': site}, 200)
    
    sites = [SiteSerializer(site).data for site in Site.objects.all()]            
    return Response({'sites': sites}, 200)


@api_view(['PUT'])
@permission_classes([IsAuthenticated, IsAllowedUser])
def set_current_site(request, site_id):
    _ = get_object_or_404(Site, id=site_id)

    request.session['current_site'] = site_id
    return Response({'message': 'Successfully set current site'}, 200)


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAllowedUser])
def add_client(request):
    serializer = ClientSerializer(data=request.data)
    if serializer.is_valid():
        
        serializer.save()
        return Response({
            'message': 'Successfully added client',
            'client': serializer.data,
        }, 201)
    return Response(serializer.errors, 400)


@api_view(['PUT'])
@permission_classes([IsAuthenticated, IsAllowedUser])
def edit_client(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    serializer = ClientSerializer(client, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response({
            'message': 'Successfully edited site', 
            'site': serializer.data,           
            }, 200)
    return Response({'message': 'Submitted data is incorrect.'}, 400)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated, IsAllowedUser])
def delete_client(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    current_site = request.session.get('current_site')

    #delete current site from session, if it is related to deleted client
    if current_site and any(site.id == current_site for site in client.sites.all()):
        del request.session['current_site']
    client.delete()
    return Response(status=204)


@api_view(['PUT'])
@permission_classes([IsAuthenticated, IsAllowedUser])
def check_linked_pages_availability(request, site_id):
    site = get_object_or_404(Site, id=site_id)
    external_links_manager = get_object_or_404(ExternalLinksManager, site=site)
    external_links_manager.clear_progress()

    unique_linked_pages = external_links_manager.get_unique_linked_pages()
    external_links_manager.update(progress_target=len(unique_linked_pages))

    for linked_page in unique_linked_pages:
        objects_to_update = external_links_manager.links.filter(linked_page=linked_page)
        for object_to_update in objects_to_update:
            object_to_update.update(is_linked_page_available=is_site_available(linked_page))
        
        external_links_manager.increase_progress()
    external_links_manager.clear_progress()
    
    return Response({'message': 'Successfully checked linked pages availability'}, 200)


@api_view(['PUT'])
@permission_classes([IsAuthenticated, IsAllowedUser])
def find_external_links(request, site_id):
    site = get_object_or_404(Site, id=site_id)
    external_links_manager, _ = ExternalLinksManager.objects.get_or_create(site=site)
    to_exclude = request.data.get('to_exclude')

    pages = get_pages_from_sitemap(site.url)
    external_links_manager.clear_progress()
    external_links_manager.delete_links()
    external_links_manager.update(progress_target=len(pages), excluded=to_exclude)
    
    for page in pages:
        links = get_external_links(page, excluded=to_exclude)
        for link in links:
            external_link_object = ExternalLink(
                linking_page=page, linked_page=link['href'], rel=link['rel'],
            )
            external_link_object.save()

            external_links_manager.links.add(external_link_object)
        external_links_manager.increase_progress()

    external_links_manager.save()
    external_links_manager.clear_progress()

    return Response({'links': ExternalLinksManagerSerializer(external_links_manager).data, 'message': 'Successfully found links'}, 200)


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAllowedUser])
def get_external_links_progress(request, site_id):
    site = get_object_or_404(Site, id=site_id)
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
        return Response(serializer.data, 201)
    return Response(serializer.errors, 400)


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAllowedUser])
def get_note(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    return Response(NoteSerializer(note).data, 200)


@api_view(['PUT'])
@permission_classes([IsAuthenticated, IsAllowedUser])
def update_note(request):
    note_id = request.data.get('note_id')
    note = get_object_or_404(Note, id=note_id)
    serializer = UpdateNoteSerializer(note, data=request.data)
    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, 200)
    
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
        return Response({'message': 'Added backlink'} | serializer.data, 201)
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
    site = get_object_or_404(Site, id=request.data.get('site_id'))
    response = []

    for backlink in site.backlinks.all():
        links_from_page = get_external_links(backlink.linking_page)
        is_active, rel = any(site.url in link['href'] for link in links_from_page), next((link['rel'] for link in links_from_page if site.url in link['href']), None)

        backlink.status_changed, backlink.active = is_active != backlink.active, is_active
        backlink.rel_changed, backlink.rel = rel != backlink.rel, rel
        backlink.save()
        response.append(BacklinkSerializer(backlink).data)

    return Response({'message': 'Updated backlinks statuses', 'links': response}, 200)


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAllowedUser])
def add_contract(request):
    serializer = ContractSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, 201)
    return Response(serializer.errors, 400)


@api_view(['PUT'])
@permission_classes([IsAuthenticated, IsAllowedUser])
def edit_contract(request, contract_id):
    contract = get_object_or_404(Contract, id=contract_id)
    serializer = ContractSerializer(contract, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, 200)
    return Response(serializer.errors, 400)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated, IsAllowedUser])
def delete_contract(request, contract_id):
    contract = get_object_or_404(Contract, id=contract_id)
    contract.delete()
    return Response(status=204)


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAllowedUser])
def add_invoice(request):
    serializer = InvoiceSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()

        return Response(serializer.data, 200)
    return Response(serializer.errors, 400)


@api_view(['PUT'])
@permission_classes([IsAuthenticated, IsAllowedUser])
def change_invoice_is_paid(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)
    invoice.is_paid = not invoice.is_paid
    invoice.save()
    return Response({'invoice': InvoiceSerializer(invoice).data})


@api_view(['DELETE'])
@permission_classes([IsAuthenticated, IsAllowedUser])
def delete_invoice(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)
    invoice.delete()
    return Response(status=204)


@api_view(['PUT'])
@permission_classes([IsAuthenticated, IsAllowedUser])
def check_contracts_urgency(request):
    contracts = Contract.objects.all()

    for contract in contracts:
        contract.is_urgent = False
        if contract.invoice_date - timedelta(days=contract.days_before_invoice_date_to_mark_urgent) <= date.today():
            contract.is_urgent = True
        contract.save()

    
    return Response({
        'contracts': ContractSerializer(Contract.objects.all(), many=True).data
        }, 200)

@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAllowedUser])
def get_client_company_info(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    if not client.is_company:
        return Response({'message': 'Client must be a company'}, 400)
    
    company_info = get_company_info(client.nip)
    if not company_info['ok']:
        return Response({
            'message': company_info['message'],
        }, 400)

    return Response({'company_info': company_info['data']}, 200)