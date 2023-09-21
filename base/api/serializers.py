from rest_framework import serializers
from ..models import Client, Site, Note, Backlink, ExternalLinksManager, Contract, Invoice
from .utils import get_domain_from_url, add_https
from dateutil.relativedelta import relativedelta



class SiteSerializer(serializers.ModelSerializer):
    client_id = serializers.IntegerField(write_only=True, required=False)
    
    class Meta:
        model = Site
        fields = ('url', 'client_id', 'logo', 'date', 'id')
        extra_kwargs = {
            'logo': {'required': False},
        }
    
    def create(self, validated_data):
        client_id = validated_data.pop('client_id', None)

        if client_id:
            client = Client.objects.get(pk=client_id)
            validated_data['url'] = get_domain_from_url(validated_data['url'])
            site = Site.objects.create(client=client, **validated_data)
            return site
        else:
            raise serializers.ValidationError("client_id is required for creating a Site")
    
    def update(self, instance, validated_data):

        instance.url = validated_data.get('url', instance.url)
        if validated_data.get('logo'):
            instance.logo = validated_data['logo']
        instance.save()
        return instance


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['name', 'nip', 'email', 'full_name', 'address', 'id', 'is_company']


class UpdateNoteSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Note
        fields = ['title', 'text']


class NoteSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Note
        fields = '__all__'


class AddNoteSerializer(serializers.ModelSerializer):
    site_id = serializers.PrimaryKeyRelatedField(queryset=Site.objects.all(), write_only=True)
    site = serializers.PrimaryKeyRelatedField(queryset=Site.objects.all(), required=False)

    class Meta:
        model = Note
        fields = ['text', 'title', 'site', 'site_id']

    def create(self, validated_data):
        site = validated_data.pop('site_id')
        note = Note.objects.create(site=site, **validated_data)
        return note
    

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
    
class BacklinkSerializer(serializers.ModelSerializer):

    class Meta:
        model = Backlink
        fields = '__all__'
    

class ExternalLinksManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExternalLinksManager
        fields = '__all__'
 

class ContractSerializer(serializers.ModelSerializer):
    site_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Contract
        fields = ['invoice_frequency', 'value', 'category', 'site_id', 'invoice_date', 'days_before_invoice_date_to_mark_urgent', 'is_urgent']
    
    def create(self, validated_data):
        site_id = validated_data.pop('site_id')
        site = Site.objects.get(id=site_id)
        contract = Contract.objects.create(site=site, **validated_data)
        contract.check_urgency()
        return contract
    
    def update(self, instance, validated_data):
        site_id = validated_data.pop('site_id')
        site = Site.objects.get(id=site_id)
        instance.site = site
        instance.check_urgency()
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        return instance
    

class InvoiceSerializer(serializers.ModelSerializer):
    contract_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Invoice
        fields = ['invoice_file', 'report_file', 'contract_id']
    
    def create(self, validated_data):
        contract_id = validated_data.pop('contract_id')
        contract = Contract.objects.get(id=contract_id)
        contract.invoice_date += relativedelta(months=+contract.invoice_frequency)
        contract.check_urgency()
        contract.save()
        invoice = Invoice.objects.create(contract=contract, **validated_data)
        return invoice

    def to_internal_value(self, data):
        if data['report_file'] == 'null':
            data['report_file'] = None

        return super(InvoiceSerializer, self).to_internal_value(data)

