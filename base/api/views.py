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
    

def format_query_attributes(query_attributes):
    if not query_attributes:
        return None
    attributes = query_attributes.split(',')
    attributes = [attribute.replace('-', '_') for attribute in attributes]
    return attributes


def format_path_attributes(path_attribute):
    if not path_attribute:
        return None
    attributes = [path_attribute.replace('-', '_')]
    return attributes


def get_attributes_from_path_or_query(path_attribute, query_attributes):
        attributes = None
        if query_attributes:
            attributes = format_query_attributes(query_attributes)
        if path_attribute:
            attributes = format_path_attributes(path_attribute)
                    
        return attributes


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

    def get(self, request, site_id=None, attribute=None, *args, **kwargs):

        if site_id:
            site = get_object_or_404(Site, id=site_id)
            attributes = get_attributes_from_path_or_query(attribute, request.GET.get('attributes'))

            if attributes:
                serializer = serializers.ExtendedSiteSerializer(site, fields=attributes)
                return Response({'site': serializer.data}, status=200)
            return Response({'site': serializers.SiteSerializer(site).data})
        
        sites = serializers.SiteSerializer(Site.objects.all(), many=True).data
        return Response({'sites': sites}, status=200)


class CurrentSiteView(APIView):
    permission_classes = [IsAuthenticated, IsAllowedUser]

    def put(self, request, *args, **kwargs):
        site_id = request.data.get('site_id', None)
        site = get_object_or_404(Site, id=site_id)

        request.session['current_site'] = site_id
        return Response({
            'site': serializers.SiteSerializer(site).data,
            'message': 'Successfully set current site',
        }, 200)
    
    def get(self, request, attribute=None, *args, **kwargs):
        site_id = request.session.get('current_site', None)
        if not site_id:
            return Response({'message': 'There is no current site set in the session'}, 404)
        
        site = get_object_or_404(Site, id=site_id)
        attributes = get_attributes_from_path_or_query(attribute, request.GET.get('attributes'))        
        if attributes:
            return Response({'site': serializers.ExtendedSiteSerializer(site, fields=attributes).data})
        
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


    def get(self, request, client_id=None, attribute=None, *args, **kwargs):
        if not client_id:
            clients = Client.objects.all()
            return Response({'clients': serializers.ClientSerializer(clients, many=True).data}, 200)
        
        client = get_object_or_404(Client, id=client_id)
        attributes = get_attributes_from_path_or_query(attribute, request.GET.get('attributes'))
        
        if attributes:
            serializer = serializers.ExtendedClientSerialzier(client, fields=attributes)
            if not serializer.data.get(attribute, None):
                return Response({'No instances found'}, 404)
            return Response({'client': serializer.data}, 200)
        
        api = request.GET.get('api', 'false').lower() == 'true' 
        if api:
            if not client.is_company:
                return Response({
                    'client': serializers.ClientSerializer(client).data,
                    'company_info': 'api=true is provided in the URL, but client is not a company'
                })
            
            company_info = get_company_info(client.nip)
            return Response({
                'client': serializers.ClientSerializer(client).data,
                'company_info': company_info['data'],
            }, 200)

        return Response({'client': serializers.ClientSerializer(client).data}, 200)


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

    def get(self, request, note_id=None, attribute=None, *args, **kwargs):
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
        attributes = get_attributes_from_path_or_query(attribute, request.GET.get('attributes'))
        if attributes:
            serializer = serializers.NoteSerializer(note, fields=attributes)

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
    
    def get(self, request, contract_id=None, attribute=None, *args, **kwargs):
        if not contract_id:
            contracts = Contract.objects.all()
            if not contracts:
                return Response({'message': 'No contracts found.'}, 404)
            
            return Response({
                'contracts': serializers.ContractSerializer(contracts, many=True).data,
            }, 200)
        
        contract = get_object_or_404(Contract, id=contract_id)
        serializer = serializers.ContractSerializer(contract)
        attributes = get_attributes_from_path_or_query(attribute, request.GET.get('attributes'))

        if attributes:
            serializer = serializers.ExtendedContractSerializer(contract, fields=attributes)

        return Response({'contract': serializer.data}, 200)
    
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
def check_contracts_urgency(request, contract_id=None):
    if not contract_id:
        contracts = Contract.objects.all()
    else:
        contracts = [get_object_or_404(Contract, id=contract_id)]
        
    for contract in contracts:
        contract.check_urgency()

    return Response({
        'message': 'Checked contracts urgency',
        'contracts': serializers.ContractSerializer(contracts, many=True).data
    }, 200)


class InvoiceView(APIView):
    permission_classes = [IsAuthenticated, IsAllowedUser]
    file_fields = ['report_file', 'invoice_file']
    
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
    
    def get(self, request, invoice_id=None, attribute=None, *args, **kwargs):
        if not invoice_id:
            invoices = Invoice.objects.all()
            serializer = serializers.InvoiceSerializer(invoices, many=True)
            return Response({'invoice': serializer.data}, 200)
        
        invoice = get_object_or_404(Invoice, id=invoice_id)
        attributes = get_attributes_from_path_or_query(attribute, request.GET.get('attributes'))
        if not attributes:
            serializer = serializers.InvoiceSerializer(invoice)
            return Response({'invoice': serializer.data}, 200)
        
        path_attributes = format_path_attributes(attribute)
        if path_attributes:
            if path_attributes[0] in self.file_fields:
                f = getattr(invoice, attribute)
                if not f:
                    return Response({'message': f"{attribute} file does not exist"}, 404)
                return FileResponse(f, as_attachment=True)
        
        serializer = serializers.InvoiceSerializer(invoice, fields=attributes)
        return Response({'invoice': serializer.data}, 200)

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
    
    def get(self, request, backlink_id=None, attribute=None, *args, **kwargs):
        if not backlink_id:
            backlinks = Backlink.objects.all()
            serializer = serializers.BacklinkSerializer(backlinks, many=True)
            return Response({'backlinks': serializer.data}, 200)
        
        backlink = get_object_or_404(Backlink, id=backlink_id)
        attributes = get_attributes_from_path_or_query(attribute, request.GET.get('attributes'))     
        if not attributes:
            serializer = serializers.BacklinkSerializer(backlink)
            return Response({'backlink': serializer.data}, 200)
        
        serializer = serializers.BacklinkSerializer(backlink, fields=attributes)
        return Response({'backlink': serializer.data}, 200)

    def delete(self, request, backlink_id, *args, **kwargs):
        backlink = get_object_or_404(Backlink, id=backlink_id)
        backlink.delete()
        return Response(status=204)


@api_view(['PUT'])
@permission_classes([IsAuthenticated, IsAllowedUser])
def update_backlinks_status_view(request, backlink_id=None, site_id=None):
    if site_id:
        site = get_object_or_404(Site, id=site_id)
        backlinks = site.backlinks.all()
    elif backlink_id:
        backlinks = [get_object_or_404(Backlink, id=backlink_id)]
    else:
        backlinks = Backlink.objects.all()

    for backlink in backlinks:
        links_from_page = get_external_links(backlink.linking_page)

        is_active = any(backlink.site.url in link['href'] for link in links_from_page)
        rel = next((link['rel'] for link in links_from_page if backlink.site.url in link['href']), None)

        backlink.status_changed = is_active != backlink.active
        backlink.active = is_active

        backlink.rel_changed = rel != backlink.rel
        backlink.rel = rel

        backlink.save()

    return Response({
        'message': 'Updated backlinks status',
        'backlinks': serializers.BacklinkSerializer(backlinks, many=True).data,
    }, 200)


class ExternalLinkView(APIView):
    permission_classes = [IsAuthenticated, IsAllowedUser]

    def put(self, request, *args, **kwargs):
        site_id = request.data.get('site_id', None)
        site = get_object_or_404(Site, id=site_id)
        external_links_manager, _ = ExternalLinksManager.objects.get_or_create(site=site)
        to_exclude = request.data.get('to_exclude', [])

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
            'external_links': serializers.ExtendedExternalLinksManagerSerializer(external_links_manager).data,
        }, 200)

    def get(self, request, external_link_id=None, attribute=None, *args, **kwargs):
        add_manager = request.GET.get('details', 'false').lower() == 'true'
        
        if external_link_id:
            external_link = get_object_or_404(ExternalLink, id=external_link_id)
            attributes = get_attributes_from_path_or_query(attribute, request.GET.get('attributes'))     
            
            if attributes:
                external_link_serializer = serializers.ExternalLinkSerializer(external_link, fields=attributes)
                return Response({'external_links': external_link_serializer.data}, 200)
                
            external_link_serializer = serializers.ExternalLinkSerializer(external_link)
            if add_manager:
                external_links_manager_serializer_data = serializers.ExternalLinksManagerSerializer(external_link.manager).data
                external_links_manager_serializer_data['external_links'] = external_link_serializer.data
                return Response({
                    'external_links_managers': external_links_manager_serializer_data,
                }, 200)
            return Response({'external_links': external_link_serializer.data}, 200)

        if add_manager:
            external_links_managers = ExternalLinksManager.objects.all()
            return Response({
                'external_links_managers': serializers.ExtendedExternalLinksManagerSerializer(external_links_managers, many=True).data
            }, 200)
        
        external_links = ExternalLink.objects.all()
        return Response({
            'external_links': serializers.ExternalLinkSerializer(external_links, many=True).data,
        }, 200)


def check_external_links_status(external_links_manager):
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
    

@api_view(['PUT'])
def update_external_links_status_view(request, site_id=None, external_link_id=None):
    if external_link_id:
        external_link = get_object_or_404(ExternalLink, id=external_link_id)
        external_link.update(is_linked_page_available=is_site_available(external_link.linked_page))
        return Response({
            'message': 'Successfully checked linked pages availability',
            'external_links': serializers.ExternalLinkSerializer(external_link).data,
        }, 200)
    
    if site_id:
        external_links_managers = [get_object_or_404(ExternalLinksManager, site_id=site_id)]
    else:
        external_links_managers = ExternalLinksManager.objects.all()
    
    for external_link_manager in external_links_managers:
        check_external_links_status(external_link_manager)    
    
    return Response({
        'message': 'Successfully checked linked pages availability',
        'external_links': serializers.ExternalLinksManagerSerializer(external_links_managers, many=True).data,
    }, 200)
