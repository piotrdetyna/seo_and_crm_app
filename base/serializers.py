from rest_framework import serializers
from .models import Client, Site, Note

class SiteSerializer(serializers.ModelSerializer):
    client_id = serializers.IntegerField(required=False)
    site_id = serializers.IntegerField(required=False)
    logo = serializers.ImageField(required=False)
    url = serializers.CharField(max_length=50)

    class Meta:
        model = Site
        fields = ['url', 'payment_date', 'logo', 'client_id', 'site_id']


class ClientSerializer(serializers.ModelSerializer):
    sites = SiteSerializer(many=True, read_only=True)

    class Meta:
        model = Client
        fields = '__all__'

class NoteSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Note
        fields = ['title', 'text']


class AddNoteSerializer(serializers.ModelSerializer):
    site_id = serializers.PrimaryKeyRelatedField(queryset=Site.objects.all(), write_only=True)
    site = serializers.PrimaryKeyRelatedField(queryset=Site.objects.all(), required=False)

    class Meta:
        model = Note
        fields = ['id', 'text', 'title', 'site', 'date', 'site_id']

    def create(self, validated_data):
        site = validated_data.pop('site_id')
        note = Note.objects.create(site=site, **validated_data)
        return note