from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import SiteSerializer, ClientSerializer
from .models import User, Client, Site, ExternalLinks, ExternalLink
from .utils.check_external_links import get_external_links
from .utils.utils import get_domain_from_url
from django.core.exceptions import ObjectDoesNotExist

def get_object_or_none(model, **kwargs):
    try:
        return model.objects.get(**kwargs)
    except ObjectDoesNotExist:
        return None

def get_value_or_none(dictionary, key):
    try:
        return dictionary[key]
    except KeyError:
        return None

    
def index(request):
    return render(request, 'base/index.html')

def external_links(request, site_id=None):
    if not site_id:
        site_id = get_value_or_none(request.session, 'current_site')

    site = get_object_or_none(Site, id=site_id)
    external_links_object = get_object_or_none(ExternalLinks, site=site)


    return render(request, 'base/external-links.html', context={
        'external_links': external_links_object,
        'site_id': site_id,
    })


@api_view(['GET', 'POST'])
def add_site(request):
    if request.method == 'GET':
        clients = Client.objects.all()
        return render(request, 'base/add-site.html', context={
            'clients': clients,
        })
    
    elif request.method == 'POST':
        serializer = SiteSerializer(data=request.data)

        if serializer.is_valid():
            client_id = serializer.validated_data['client_id']
            client = Client.objects.get(id=client_id)
            url = get_domain_from_url(serializer.validated_data['url'])
            site = Site(
                url=url,
                payment_date=serializer.validated_data['payment_date'],
                client=client,
                logo=serializer.validated_data['logo'],
            )
            site.save()
            return Response('Successfully added site', 200)
        return Response('Submitted data is incorrect.', 400)


@api_view(['GET'])
def site_details(request, site_id):
    site = Site.objects.get(id=site_id)
    site.payment_date = site.payment_date.strftime('%Y-%m-%d')       
    return render(request, 'base/site-details.html', context={
        'site': site,
    })


@api_view(['PUT', 'DELETE'])
def edit_site(request):
    if request.method == 'PUT':
        serializer = SiteSerializer(data=request.data)
        if serializer.is_valid():
            url = get_domain_from_url(serializer.validated_data['url'])
            site = Site.objects.get(id=serializer.validated_data['site_id'])

            site.url = url
            site.payment_date = serializer.validated_data['payment_date']

            if 'logo' in serializer.validated_data:
                site.logo=serializer.validated_data['logo']

            site.save()

            return Response('Successfully edited site', 200)
        return Response('Submitted data is incorrect.', 400)


@api_view(['PUT'])
def find_external_links(request):
    site_id = request.data['site_id']
    site = Site.objects.get(id=site_id)

    to_exclude = request.data['to_exclude']
    links = get_external_links(site.url, excluded=to_exclude)
    
    external_link_objects = []

    for linking_page, linked_page in links.items():
        for link in linked_page:
            external_link = ExternalLink(
                linking_page=linking_page,
                linked_page=link['href'],
                rel=link['rel']
            )
            external_link.save()
            external_link_objects.append(external_link)
    
    external_links_object, created = ExternalLinks.objects.get_or_create(site=site, defaults={'excluded': to_exclude})
    external_links_object.save()
    external_links_object.links.set(external_link_objects)
    external_links_object.excluded = to_exclude
    external_links_object.save()

    return Response({'links': links}, status=200)
        
    
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
    site_id = request.data['site_id']
    try:
        site = Site.objects.get(id=site_id)
        request.session['current_site'] = site_id
    except ObjectDoesNotExist:
        return Response('Site is not valid', 400)
    return Response('Successfully setted current site', 200)
