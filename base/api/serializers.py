from rest_framework import serializers
from ..models import Client, Site, Note, Backlink, Keyword, Check, ExternalLinksManager, ExternalLink, Contract, Invoice, User
from .utils import get_domain_from_url, add_https
from dateutil.relativedelta import relativedelta
from django.shortcuts import get_object_or_404
from copy import copy


class DynamicFieldsSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)
        super(DynamicFieldsSerializer, self).__init__(*args, **kwargs)
        
        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field in allowed:
                if field not in existing:
                    raise(serializers.ValidationError(f'{field} is not valid field'))
            
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['name', 'nip', 'email', 'full_name', 'address', 'id', 'is_company']


class EditClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['name', 'nip', 'email', 'full_name', 'address', 'is_company']
        extra_kwargs = {field: {'required': False} for field in fields}
    

class EditSiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Site
        fields = ('url', 'logo')
        extra_kwargs = {field: {'required': False} for field in fields}


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'id']


class NoteSerializer(DynamicFieldsSerializer):
    site_id = serializers.IntegerField(write_only=True, required=False)
    
    class Meta:
        model = Note
        fields = ['text', 'title', 'site_id', 'id', 'date']

    def create(self, validated_data):
        site_id = validated_data.pop('site_id')
        site = get_object_or_404(Site, id=site_id)
        note = Note.objects.create(site=site, **validated_data)
        return note
    
class EditNoteSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = Note
        fields = ['text', 'title']
        extra_kwargs = {field: {'required': False} for field in fields}


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(max_length=150)


class AddBacklinkSerializer(serializers.ModelSerializer):
    site_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Backlink
        fields = ['linking_page', 'site_id']

    def create(self, validated_data):
        site_id = validated_data.pop('site_id')
        site = Site.objects.get(id=site_id)
        validated_data['linking_page'] = add_https(validated_data['linking_page'])
        backlink = Backlink.objects.create(site=site, **validated_data)
        return backlink
    

class BacklinkSerializer(DynamicFieldsSerializer):
    site_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Backlink
        fields = '__all__'
        extra_kwargs = {
            'site': {'read_only': True},
            'active': {'read_only': True},
            'rel': {'read_only': True},
            'rel_changed': {'read_only': True},
            'status_changed': {'read_only': True},
        }

    def create(self, validated_data):
        site_id = validated_data.pop('site_id')
        site = Site.objects.get(id=site_id)
        validated_data['linking_page'] = add_https(validated_data['linking_page'])
        backlink = Backlink.objects.create(site=site, **validated_data)
        return backlink
    

class ExternalLinkSerializer(DynamicFieldsSerializer):
    class Meta:
        model = ExternalLink
        fields = '__all__'
    
    
class ExternalLinksManagerSerializer(serializers.ModelSerializer):
    external_links = ExternalLinkSerializer(read_only=True, many=True, fields=['id'])
    class Meta:
        model = ExternalLinksManager
        fields = '__all__'


class ExtendedExternalLinksManagerSerializer(DynamicFieldsSerializer):
    external_links = ExternalLinkSerializer(read_only=True, many=True)
    class Meta:
        model = ExternalLinksManager
        fields = '__all__'
 

class ContractSerializer(serializers.ModelSerializer):
    site_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Contract
        fields = ['invoice_frequency', 'value', 'category', 'site_id', 'invoice_date', 'days_before_invoice_date_to_mark_urgent', 'is_urgent', 'id']
    
    def create(self, validated_data):
        site_id = validated_data.pop('site_id')
        site = Site.objects.get(id=site_id)
        contract = Contract.objects.create(site=site, **validated_data)
        contract.check_urgency()
        return contract
    
    
class EditContractSerializer(serializers.ModelSerializer):
    site_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Contract
        fields = ['invoice_frequency', 'site_id', 'value', 'category', 'invoice_date', 'days_before_invoice_date_to_mark_urgent', 'is_urgent']
        extra_kwargs = {field: {'required': False} for field in fields}
    
    def update(self, instance, validated_data):
        site_id = validated_data.pop('site_id')
        site = Site.objects.get(id=site_id)
        instance.site = site
        instance.check_urgency()
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        return instance
     

class InvoiceSerializer(DynamicFieldsSerializer):
    contract_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Invoice
        fields = ['invoice_file', 'report_file', 'contract_id', 'is_paid', 'id', 'payment_date']
    
    def create(self, validated_data):
        contract_id = validated_data.pop('contract_id')
        contract = Contract.objects.get(id=contract_id)
        contract.invoice_date += relativedelta(months=+contract.invoice_frequency)
        contract.check_urgency()
        contract.save()
        invoice = Invoice.objects.create(contract=contract, **validated_data)
        invoice.check_overduity()
        return invoice
    

class EditInvoiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Invoice
        fields = ['is_paid', 'invoice_file', 'report_file', 'payment_date']
        extra_kwargs = {field: {'required': False} for field in fields}
    
    def to_internal_value(self, data):
        #set every value which is equal to 'null' to None
        data = copy(data)
        for key, value in data.items():
            if value == 'null':
                data[key] = None

        return super().to_internal_value(data)


class SiteSerializer(serializers.ModelSerializer):
    client_id = serializers.IntegerField(write_only=True)
    

    class Meta:
        model = Site
        fields = '__all__'
        extra_kwargs = {
            'client': {'read_only': True},
        }

    
    def create(self, validated_data):
        client_id = validated_data.pop('client_id', None)
        client = Client.objects.get(pk=client_id)

        site = Site.objects.create(client=client, **validated_data)
        return site

    def to_internal_value(self, data):
        data = copy(data)
        data['url'] = get_domain_from_url(data['url'])
        return super().to_internal_value(data)
    

class ExtendedSiteSerializer(DynamicFieldsSerializer):
    contracts = ContractSerializer(many=True)
    notes = NoteSerializer(many=True)
    external_links_manager = ExtendedExternalLinksManagerSerializer()
    backlinks = BacklinkSerializer(many=True)
    client = ClientSerializer()

    class Meta:
        model = Site
        fields = '__all__'


class ExtendedClientSerialzier(DynamicFieldsSerializer):
    sites = SiteSerializer(many=True)

    class Meta:
        model = Client
        fields = ['name', 'nip', 'email', 'full_name', 'address', 'id', 'is_company', 'sites']


class ExtendedContractSerializer(DynamicFieldsSerializer):
    invoices = InvoiceSerializer(many=True)

    class Meta:
        model = Contract
        fields = ['invoice_frequency', 'value', 'category', 'invoice_date', 'days_before_invoice_date_to_mark_urgent', 'is_urgent', 'invoices', 'id']


class CheckSerializer(serializers.ModelSerializer):
    class Meta:
        model = Check
        fields = '__all__'


class KeywordSerializer(serializers.ModelSerializer):
    site_id = serializers.IntegerField(write_only=True)
    position = serializers.SerializerMethodField()

    class Meta:
        model = Keyword
        fields = '__all__'
        extra_kwargs = {
            'site': {'read_only': True},
        }
    
    def create(self, validated_data):
        site_id = validated_data.pop('site_id', None)
        site = Site.objects.get(id=site_id)

        keyword = Keyword.objects.create(site=site, **validated_data)
        return keyword
    
    def get_position(self, obj):
        return obj.latest_check().position


class ExtendedKeywordSerializer(DynamicFieldsSerializer):
    checks = CheckSerializer(many=True)
    position = serializers.SerializerMethodField()

    class Meta:
        model = Keyword
        fields = '__all__'

    def get_position(self, obj):
        return obj.latest_check().position


STATIC_SERIALIZERS = {
    Site: SiteSerializer,
    Client: ClientSerializer,
    Note: NoteSerializer,
    Backlink: BacklinkSerializer,
    ExternalLink: ExternalLinkSerializer,
    ExternalLinksManager: ExternalLinksManagerSerializer,
    Invoice: InvoiceSerializer,
    Contract: ContractSerializer,
    User: UserSerializer,
    Keyword: KeywordSerializer,
}

DYNAMIC_SERIALIZERS = {
    Site: ExtendedSiteSerializer,
    Client: ExtendedClientSerialzier,
    Note: NoteSerializer,
    Backlink: BacklinkSerializer,
    ExternalLink: ExternalLinkSerializer,
    ExternalLinksManager: ExtendedExternalLinksManagerSerializer,
    Invoice: InvoiceSerializer,
    Contract: ExtendedContractSerializer,
    Keyword: ExtendedKeywordSerializer,
}