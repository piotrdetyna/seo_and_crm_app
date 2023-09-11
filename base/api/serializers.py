from rest_framework import serializers
from ..models import Client, Site, Note, Backlink
from .utils import get_domain_from_url

class AddSiteSerializer(serializers.ModelSerializer):
    client_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Site
        fields = ('url', 'payment_date', 'client_id', 'logo', 'date')

    def create(self, validated_data):
        client_id = validated_data.pop('client_id')
        client = Client.objects.get(pk=client_id)
        validated_data['url'] = get_domain_from_url(validated_data['url'])
        site = Site.objects.create(client=client, **validated_data)
        return site
    

class UpdateSiteSerializer(serializers.ModelSerializer):
    site_id = serializers.IntegerField(write_only=True, required=True)

    class Meta:
        model = Site
        fields = ('url', 'payment_date', 'logo', 'site_id')
        extra_kwargs = {
            'logo': {'required': False}
        }

    def update(self, instance, validated_data):
        instance.url = validated_data.get('url', instance.url)
        instance.payment_date = validated_data.get('payment_date', instance.payment_date)

        if validated_data.get('logo'):
            instance.logo = validated_data['logo']

        instance.save()
        return instance


class ClientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Client
        fields = ['name', 'nip', 'email']

class NoteSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Note
        fields = ['title', 'text']


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
        backlink = Backlink.objects.create(site=site, **validated_data)
        return backlink