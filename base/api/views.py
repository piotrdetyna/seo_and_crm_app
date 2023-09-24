from . import serializers
from .utils import get_external_links, get_pages_from_sitemap, is_site_available, get_company_info
from ..models import Site, ExternalLinksManager, ExternalLink, Note, Backlink, Client, Contract, Invoice
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login, logout
from rest_framework.permissions import IsAuthenticated, BasePermission
from crm.settings import ALLOWED_USERS
from django.http import FileResponse
from rest_framework.views import APIView




class IsAllowedUser(BasePermission):

    def has_permission(self, request, view):
        return request.user.username in ALLOWED_USERS


class SiteView(APIView):
    permission_classes = [IsAuthenticated, IsAllowedUser]

    def post(self, request, *args, **kwargs):
        serializer = serializers.SiteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Successfully added site',
                'site': serializer.data,
            }, status=201)
        return Response({
            'message': 'Submitted data is incorrect.',
            'errors': serializer.errors
        }, status=400)

    def patch(self, request, site_id=None, *args, **kwargs):
        site = get_object_or_404(Site, id=site_id)
        serializer = serializers.EditSiteSerializer(site, data=request.data)
        if serializer.is_valid():
            site = serializer.save()
            return Response({
                'message': 'Successfully edited site',
                'site': serializers.SiteSerializer(site).data,
            }, status=200)
        return Response({
            'message': 'Submitted data is incorrect.',
            'errors': serializer.errors
        }, status=400)

    def delete(self, request, site_id=None, *args, **kwargs):
        site = get_object_or_404(Site, id=site_id)
        if site_id == request.session.get('current_site'):
            del request.session['current_site']
        site.delete()
        return Response(status=204)

    def get(self, request, site_id=None, *args, **kwargs):
        if site_id:
            site = serializers.SiteSerializer(get_object_or_404(Site, id=site_id)).data
            return Response({'site': site}, status=200)
        
        sites = serializers.SiteSerializer(Site.objects.all(), many=True).data
        return Response({'sites': sites}, status=200)


class CurrentSiteView(APIView):
    permission_classes = [IsAuthenticated, IsAllowedUser]

    def put(self, request, site_id, *args, **kwargs):
        site = get_object_or_404(Site, id=site_id)

        request.session['current_site'] = site_id
        return Response({
            'site': serializers.SiteSerializer(site).data,
            'message': 'Successfully set current site',
        }, 200)
    
    def get(self, request, *args, **kwargs):
        site_id = request.session.get('current_site', None)
        if not site_id:
            return Response({'message': 'There is no current site set in the session'}, 404)
        
        site = get_object_or_404(Site, id=site)

        return Response({'site': serializers.SiteSerializer(site).data})
    
    def delete(self, request, *args, **kwargs):
        site_id = request.session.get('current_site', None)
        if not site_id:
            return Response({'message': 'There is no current site set in the session'}, 404)
        
        del request.session['current_site']
        return Response(status=204)


class ClientView(APIView):
    permission_classes = [IsAuthenticated, IsAllowedUser]

    def post(self, request, *args, **kwargs):
        serializer = serializers.ClientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Successfully added client',
                'client': serializer.data,
            }, 201)
        
        return Response({
            'message': 'Submitted data is incorrect.',
            'errors': serializer.errors,
        }, 400)

    def patch(self, request, client_id, *args, **kwargs):
        client = get_object_or_404(Client, id=client_id)
        serializer = serializers.EditClientSerializer(client, data=request.data)
        if serializer.is_valid():
            client = serializer.save()
            return Response({
                'message': 'Successfully edited site',
                'client': serializers.ClientSerializer(client).data,
            }, 200)
        
        return Response({
            'message': 'Submitted data is incorrect.',
            'errors': serializer.errors,
        }, 400)

    def delete(self, request, client_id, *args, **kwargs):
        client = get_object_or_404(Client, id=client_id)
        current_site = request.session.get('current_site')
        if any(site.id == current_site for site in client.sites.all()):
            del request.session['current_site']
        client.delete()
        return Response(status=204)

    def get(self, request, client_id, *args, **kwargs):
        client = get_object_or_404(Client, id=client_id)
        api = request.query_params.get('api', 'true').lower() == 'false'  

        if not client.is_company or not api:
            return Response({'client': {serializers.ClientSerializer(client).data}}, 200)


        company_info = get_company_info(client.nip)
        if not company_info['ok']:
            return Response({
                'message': company_info['message'],
            }, 400)

        return Response({
            'client': serializers.ClientSerializer(client).data,
            'client_info': company_info['data'],
        }, 200)
    

class NoteView(APIView):
    permission_classes = [IsAuthenticated, IsAllowedUser]

    def post(self, request, *args, **kwargs):
        serializer = serializers.NoteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Successfully added a note',
                'note': serializer.data,
            }, 201)
        return Response({
            'message': 'Submitted data is incorrect.',
            'errors': serializer.errors,
        }, 400)

    def get(self, request, note_id=None, *args, **kwargs):
        if not note_id:
            notes = Note.objects.all()
            if not notes:
                return Response({'message': 'No notes found.'}, 404)
            
            return Response({
                'message': 'Successfully retrieved notes',
                'notes': serializers.NoteSerializer(notes, many=True).data
            }, 200)
        
        note = get_object_or_404(Note, id=note_id)
        serializer = serializers.NoteSerializer(note)
        return Response({
            'message': 'Successfully retrieved note',
            'note': serializer.data,
        }, 200)

    def patch(self, request, note_id=None, *args, **kwargs):
        note = get_object_or_404(Note, id=note_id)
        serializer = serializers.EditNoteSerializer(note, data=request.data)
        if serializer.is_valid():
            note = serializer.save()
            return Response({
                'message': 'Successfully updated note',
                'note': serializers.NoteSerializer(note).data,
            }, 201)
        return Response({
            'message': 'Submitted data is incorrect.',
            'errors': serializer.errors,
        }, 400)

    def delete(self, request, note_id=None, *args, **kwargs):
        note = get_object_or_404(Note, id=note_id)
        note.delete()
        return Response(204)
    

class ContractView(APIView):
    permission_classes = [IsAuthenticated, IsAllowedUser]

    def post(self, request, *args, **kwargs):
        serializer = serializers.ContractSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Successfully added contract.',
                'contract': serializer.data,
            }, 201)
        
        return Response({
            'message': 'Submitted data is incorrect.',
            'errors': serializer.errors,
        }, 400)
    
    def get(self, request, contract_id=None, *args, **kwargs):
        if not contract_id:
            contracts = Contract.objects.all()
            if not contracts:
                return Response({'message': 'No contracts found.'}, 404)
            
            return Response({
                'contracts': serializers.ContractSerializer(contracts, many=True).data,
            }, 200)
        
        contract = get_object_or_404(Contract, id=contract_id)
        return Response({'contract': serializers.ContractSerializer(contract).data}, 200)
        
    
    def patch(self, request, contract_id, *args, **kwargs):
        contract = get_object_or_404(Contract, id=contract_id)
        serializer = serializers.EditContractSerializer(contract, data=request.data)
        if serializer.is_valid():
            contract = serializer.save()
            contract.check_urgency()
            return Response({
                'message': 'Successfully edited contract.',
                'contract': serializers.ContractSerializer(contract).data,
            }, status=200)
        
        return Response({
            'message': 'Submitted data is incorrect.',
            'errors': serializer.errors,
        }, 400)

    def delete(self, request, contract_id, *args, **kwargs):
        contract = get_object_or_404(Contract, id=contract_id)
        contract.delete()
        return Response(204)


@api_view(['PUT'])
@permission_classes([IsAuthenticated, IsAllowedUser])
def check_contracts_urgency(request):
    contracts = Contract.objects.all()
    for contract in contracts:
        contract.check_urgency()
    
    return Response({
        'contracts': serializers.ContractSerializer(Contract.objects.all(), many=True).data
    }, 200)


class InvoiceView(APIView):
    permission_classes = [IsAuthenticated, IsAllowedUser]
    
    def post(self, request, *args, **kwargs):
        serializer = serializers.InvoiceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Successfully added invoice.',
                'invoice': serializer.data,
            }, 201)
        
        return Response({
            'message': 'Submitted data is incorrect.',
            'errors': serializer.errors,
        }, 400)
    
    def delete(self, request, invoice_id, *args, **kwargs):
        invoice = get_object_or_404(Invoice, id=invoice_id)
        invoice.delete()
        return Response(status=204)
    
    def patch(self, request, invoice_id, *args, **kwargs):
        invoice = get_object_or_404(Invoice, id=invoice_id)
        serializer = serializers.EditInvoiceSerializer(invoice, data=request.data)
        
        if serializer.is_valid():
            invoice = serializer.save()
            return Response({
                'message': 'Successfully edited invoice.',
                'invoice': serializers.InvoiceSerializer(invoice).data
            }, 200)
        
        return Response({
            'message': 'Submitted data is incorrect.',
            'errors': serializer.errors,
        }, 400)


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAllowedUser])
def invoice_get_file(request, invoice_id, file_type):
    invoice = get_object_or_404(Invoice, id=invoice_id)
    if not file_type in ['invoice_file', 'report_file']:
        return Response({'message': 'Invalid file field'}, 400)
   
    try:
        f = getattr(invoice, file_type)
        return FileResponse(f, as_attachment=True)
    except FileNotFoundError:
        return Response({'message': "File does not exist"}, 404)


@api_view(['PUT'])
@permission_classes([IsAuthenticated, IsAllowedUser])
def check_linked_pages_availability(request, site_id):
    site = get_object_or_404(Site, id=site_id)
    external_links_manager = get_object_or_404(ExternalLinksManager, site=site)

    external_links_manager.clear_progress()

    unique_linked_pages = external_links_manager.get_unique_linked_pages()
    external_links_manager.update(progress_target=len(unique_linked_pages))

    for linked_page in unique_linked_pages:

        #update every ExternalLink object where linked_page is equal to current unique page
        objects_to_update = external_links_manager.links.filter(linked_page=linked_page)
        for object_to_update in objects_to_update:
            object_to_update.update(is_linked_page_available=is_site_available(linked_page))
        
        external_links_manager.increase_progress()
    external_links_manager.clear_progress()
    
    return Response({
        'message': 'Successfully checked linked pages availability',
        'external_links': serializers.ExternalLinksManagerSerializer(external_links_manager).data,
    }, 200)


@api_view(['POST'])
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
                manager = external_links_manager,
                linking_page=page, 
                linked_page=link['href'], 
                rel=link['rel'],
            )
            external_link_object.save()

        external_links_manager.increase_progress()
    external_links_manager.clear_progress()

    return Response({
        'message': 'Successfully found links', 
        'external_links': serializers.ExternalLinksManagerSerializer(external_links_manager).data,
    }, 200)


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
def login_view(request):
    serializer = serializers.LoginSerializer(data=request.data)
    if not serializer.is_valid():
        return Response({
            'message': 'Submitted data is not valid',
            'errors': serializer.errors,
        }, 400)
    
    user = authenticate(
        request._request, 
        username=serializer.validated_data['username'], 
        password=serializer.validated_data['password'],
    )

    if user is not None:
        login(request._request, user)
        return Response({
            'message': 'Successfully logged in',
            'user': serializers.UserSerializer(user).data,
        }, 200)
    return Response({'message': 'Incorrect username or password'}, 400)
    

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    logout(request._request)
    return Response(status=204)


class BacklinkView(APIView):
    permission_classes = [IsAuthenticated, IsAllowedUser]

    def post(self, request, *args, **kwargs):
        serializer = serializers.BacklinkSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Added backlink',
                'backlink': serializer.data,
            }, 201)
        
        return Response({
            'message': 'Submitted data is incorrect.',
            'errors': serializer.errors,
        }, 400)

    def delete(self, request, backlink_id, *args, **kwargs):
        backlink = get_object_or_404(Backlink, id=backlink_id)
        backlink.delete()
        return Response(status=204)


@api_view(['PUT'])
@permission_classes([IsAuthenticated, IsAllowedUser])
def check_backlinks_status(request, site_id):
    site = get_object_or_404(Site, id=site_id)

    for backlink in site.backlinks.all():
        links_from_page = get_external_links(backlink.linking_page)

        is_active = any(site.url in link['href'] for link in links_from_page)
        rel = next((link['rel'] for link in links_from_page if site.url in link['href']), None)

        backlink.status_changed = is_active != backlink.active
        backlink.active = is_active

        backlink.rel_changed = rel != backlink.rel
        backlink.rel = rel

        backlink.save()

    return Response({
        'message': 'Updated backlinks status',
        'backlinks': serializers.BacklinkSerializer(site.backlinks.all(), many=True).data,
    }, 200)






