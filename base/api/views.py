from . import serializers
from .utils import get_external_links, get_pages_from_sitemap, is_site_available, get_company_info, get_domain_expiry_date
from ..models import Site, ExternalLinksManager, Keyword, Check, ExternalLink, Note, Backlink, Client, Contract, Invoice
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404, get_list_or_404
from django.contrib.auth import authenticate, login, logout
from rest_framework.permissions import IsAuthenticated, BasePermission
from crm.settings import ALLOWED_USERS
from django.http import FileResponse
from rest_framework.views import APIView
from django.db.models.base import ModelBase
from time import sleep

class IsAllowedUser(BasePermission):

    def has_permission(self, request, view):
        return request.user.username in ALLOWED_USERS
    

def get_query_attributes(query_attributes):
    if not query_attributes:
        return None
    attributes = query_attributes.split(',')
    attributes = [attribute.replace('-', '_') for attribute in attributes]
    return attributes


def get_accurate_serializer(object_or_model, attributes=None):

    #if Model is passed return its objects serializer
    if type(object_or_model) == ModelBase:
        model = object_or_model

        objects = get_list_or_404(model)
        serializer_class = serializers.STATIC_SERIALIZERS[model]
        serializer = serializer_class(objects, many=True)
        return serializer
    
    model_object = object_or_model
    model = type(model_object)
    if attributes:
        serializer_class = serializers.DYNAMIC_SERIALIZERS[model]
        serializer = serializer_class(model_object, fields=attributes)
    else:
        serializer_class = serializers.STATIC_SERIALIZERS[model]
        serializer = serializer_class(model_object)
    return serializer    


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
        if not site_id:
            serializer = get_accurate_serializer(Site)
            return Response({'sites': serializer.data}, 200)

        site = get_object_or_404(Site, id=site_id)
        attributes = get_query_attributes(request.GET.get('attributes'))
        serializer = get_accurate_serializer(site, attributes)
        return Response({'sites': serializer.data})
        

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
    
    def get(self, request, *args, **kwargs):
        site_id = request.session.get('current_site', None)
        if not site_id:
            return Response({'message': 'There is no current site set in the session'}, 404)
        
        site = get_object_or_404(Site, id=site_id)
        attributes = get_query_attributes(request.GET.get('attributes'))
        serializer = get_accurate_serializer(site, attributes)
        return Response({'sites': serializer.data})
    
    def delete(self, request, *args, **kwargs):
        site_id = request.session.get('current_site', None)
        if not site_id:
            return Response({'message': 'There is no current site set in the session'}, 404)
        
        del request.session['current_site']
        return Response(status=204)
    

@api_view(['PUT'])
@permission_classes([IsAuthenticated, IsAllowedUser])
def check_domain_expiry(request, site_id=None):
    if site_id:
        sites = [get_object_or_404(Site, id=site_id)]
    else:
        sites = Site.objects.all()
    
    errors = 0
    for site in sites:
        site.domain_expiry_date = get_domain_expiry_date(site.url)
        if not site.domain_expiry_date:
            errors += 1
        else:
            site.save()

    if errors == 0:
        message = f'Successfully checked {len(sites)} sites expiry date. Unsuccessful attempts: {errors}'
        status = 200
    elif errors == len(sites):
        message = f'Tried to check {len(sites)} sites, but no one of them was a successfull attempt'
        status = 424
    else:
        message = f'Successfully checked {len(sites) - errors} sites expiry date. Unsuccessful attempts: {errors}'
        status = 207
        
    return Response({
        'message': message,
        'sites': serializers.SiteSerializer(sites, many=True).data
    }, status)




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


    def get(self, request, client_id=None, *args, **kwargs):
        if not client_id:
            serializer = get_accurate_serializer(Client)
            return Response({'clients': serializer.data}, 200)

        client = get_object_or_404(Client, id=client_id)
        attributes = get_query_attributes(request.GET.get('attributes'))
        serializer = get_accurate_serializer(client, attributes)
        
        get_company_info_from_api = request.GET.get('api', 'false').lower() == 'true' 
        if get_company_info_from_api:
            if not client.is_company:
                company = {'error': 'api=true is provided in the URL, but client is not a company'}
            else:
                company = get_company_info(client.nip)['data']

            return Response({
                'client': serializer.data,
                'company': company,
            }, 200)

        return Response({'clients': serializer.data}, 200)


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
            serializer = get_accurate_serializer(Note)            
            return Response({'notes': serializer.data}, 200)
        
        note = get_object_or_404(Note, id=note_id)
        attributes = get_query_attributes(request.GET.get('attributes'))
        serializer = get_accurate_serializer(note, attributes)
        return Response({'notes': serializer.data}, 200)

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
            serializer = get_accurate_serializer(Contract)            
            return Response({'contracts': serializer.data}, 200)
        
        contract = get_object_or_404(Contract, id=contract_id)
        attributes = get_query_attributes(request.GET.get('attributes'))
        serializer = get_accurate_serializer(contract, attributes)
        return Response({'contracts': serializer.data}, 200)
    
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
        contracts = get_list_or_404(Contract)
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
    
    def get(self, request, invoice_id=None, *args, **kwargs):
        if not invoice_id:
            serializer = get_accurate_serializer(Invoice)
            return Response({'invoices': serializer.data}, 200)
        

        invoice = get_object_or_404(Invoice, id=invoice_id)
        attributes = get_query_attributes(request.GET.get('attributes'))
        
        # check if at least one field should return a file
        for attribute in attributes:
            if attribute in self.file_fields:
                f = getattr(invoice, attribute)
                if not f:
                    return Response({'message': f"{attribute} file does not exist"}, 404)
                return FileResponse(f, as_attachment=True)
            
        serializer = get_accurate_serializer(invoice, attributes)
        return Response({'invoices': serializer.data}, 200)

    def delete(self, request, invoice_id, *args, **kwargs):
        invoice = get_object_or_404(Invoice, id=invoice_id)
        invoice.delete()
        return Response(status=204)
    
    def patch(self, request, invoice_id, *args, **kwargs):
        invoice = get_object_or_404(Invoice, id=invoice_id)
        serializer = serializers.EditInvoiceSerializer(invoice, data=request.data)
        
        if serializer.is_valid():
            invoice.check_overduity()
            invoice = serializer.save()
            return Response({
                'message': 'Successfully edited invoice.',
                'invoice': serializers.InvoiceSerializer(invoice).data
            }, 200)
        
        return Response({
            'message': 'Submitted data is incorrect.',
            'errors': serializer.errors,
        }, 400)
    

@api_view(['PUT'])
@permission_classes([IsAuthenticated, IsAllowedUser])
def update_invoice_overduity(request, invoice_id=None):
    if invoice_id:
        invoice = get_object_or_404(Invoice, id=invoice_id)
        invoice.check_overduity()
        return Response({
            'message': 'Checked invoice overduity',
            'invoices': serializers.InvoiceSerializer(invoice).data,
        }, 200)
    
    invoices = get_list_or_404(Invoice)
    for invoice in invoices:
        invoice.check_overduity()
    return Response({
        'message': 'Checked invoices overduity',
        'invoices': serializers.InvoiceSerializer(invoices, many=True).data,
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
    
    def get(self, request, backlink_id=None, *args, **kwargs):
        if not backlink_id:
            serializer = get_accurate_serializer(Backlink)
            return Response({'backlinks': serializer.data}, 200)
        
        backlink = get_object_or_404(Backlink, id=backlink_id)
        attributes = get_query_attributes(request.GET.get('attributes'))
        serializer = get_accurate_serializer(backlink, attributes)
        return Response({'backlinks': serializer.data}, 200)

    def delete(self, request, backlink_id, *args, **kwargs):
        backlink = get_object_or_404(Backlink, id=backlink_id)
        backlink.delete()
        return Response(status=204)


@api_view(['PUT'])
@permission_classes([IsAuthenticated, IsAllowedUser])
def update_backlinks_status_view(request, backlink_id=None):
    site_id = request.GET.get('site', None)
    if site_id:
        site = get_object_or_404(Site, id=site_id)
        backlinks = site.backlinks.all()
    elif backlink_id:
        backlinks = [get_object_or_404(Backlink, id=backlink_id)]
    else:
        backlinks = get_list_or_404(Backlink)

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


class ExternalLinksManagersView(APIView):
    permission_classes = [IsAuthenticated, IsAllowedUser]

    def put(self, request, site_id, *args, **kwargs):
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

    def get(self, request, site_id=None, *args, **kwargs):      
        if not site_id:
            serializer = get_accurate_serializer(ExternalLinksManager)
            return Response({'external_links_managers': serializer.data}, 200)

        external_links_manager = get_object_or_404(ExternalLinksManager, site_id=site_id)
        attributes = get_query_attributes(request.GET.get('attributes'))  
        serializer = get_accurate_serializer(external_links_manager, attributes)
        return Response({'external_links_managers': serializer.data}, 200)
    


def check_external_links_status(external_links_manager):
    external_links_manager.clear_progress()
    unique_linked_pages = external_links_manager.get_unique_linked_pages()
    external_links_manager.update(progress_target=len(unique_linked_pages))

    for linked_page in unique_linked_pages:
        #update every ExternalLink object where linked_page is equal to current unique page
        objects_to_update = external_links_manager.external_links.filter(linked_page=linked_page)
        for object_to_update in objects_to_update:
            object_to_update.update(is_linked_page_available=is_site_available(linked_page))
        
        external_links_manager.increase_progress()
    external_links_manager.clear_progress()
    

@api_view(['PUT'])
@permission_classes([IsAuthenticated, IsAllowedUser])
def update_external_links_status_view(request, site_id=None):
    
    if site_id:
        external_links_managers = [get_object_or_404(ExternalLinksManager, site_id=site_id)]
    else:
        external_links_managers = get_list_or_404(ExternalLinksManager)
    
    for external_link_manager in external_links_managers:
        check_external_links_status(external_link_manager)    
    
    return Response({
        'message': 'Successfully checked linked pages availability',
        'external_links_managers': serializers.ExternalLinksManagerSerializer(external_links_managers, many=True).data,
    }, 200)


class KeywordView(APIView):
    permission_classes = [IsAuthenticated, IsAllowedUser]

    def post(self, request, *args, **kwargs):
        serializer = serializers.KeywordSerializer(data=request.data)
        if serializer.is_valid():
            keyword = serializer.save()
            keyword.new_check()

            return Response({
                'message': 'Successfully added keyword',
                'keywords': serializer.data,
            }, 201)
        
        return Response({
            'message': 'Submitted data is incorrect.',
            'errors': serializer.errors
        }, 400)
    
    def get(self, request, keyword_id=None, *args, **kwargs):
        if not keyword_id:
            serializer = get_accurate_serializer(Keyword)
            return Response({'keywords': serializer.data}, 200)
        
        keyword = get_object_or_404(Keyword, id=keyword_id)
        attributes = get_query_attributes(request.GET.get('attributes'))
        serializer = get_accurate_serializer(keyword, attributes)
        return Response({'keywords': serializer.data}, 200)
    
    def delete(self, request, keyword_id, *args, **kwargs):
        keyword = get_object_or_404(Keyword, id=keyword_id)
        keyword.delete()
        return Response(status=204)
    
@api_view(['PUT'])
@permission_classes([IsAuthenticated, IsAllowedUser])
def check_keyword_position(request, keyword_id=None):
    site_id = request.GET.get('site', None)
    if site_id:
        site = get_object_or_404(Site, id=site_id)
        keywords = site.keywords.all()
    elif keyword_id:
        keywords = [get_object_or_404(Keyword, id=keyword_id)]
    else:
        keywords = get_list_or_404(Keyword)
    
    for keyword in keywords:
        keyword.new_check()
        sleep(1)

    return Response({
        'message': 'Checked positions',
        'keywords': serializers.ExtendedKeywordSerializer(keywords, many=True).data,
    }, 200)


