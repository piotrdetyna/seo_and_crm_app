from django.db import models
from django.contrib.auth.models import AbstractUser
from slugify import slugify
from django.contrib.contenttypes.fields import GenericForeignKey, ContentType


def logo_file_name(instance, filename):
    return '/'.join(['sites', slugify(instance.url), 'logo.'+ filename.split('.')[-1]])


class User(AbstractUser):
    pass


class Client(models.Model):
    name = models.CharField(max_length=100)
    nip = models.IntegerField()
    email = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Site(models.Model):
    url = models.CharField(max_length=150, unique=True)
    payment_date = models.DateField(blank=True, null=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="sites")
    logo = models.ImageField(upload_to=logo_file_name)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.url
    
    def as_json(self):
        return {
            'url': self.url,
            'payment_date': self.payment_date,
            'client': self.client.name,
            'logo': self.logo.url,
            'date': self.date,
            'id': self.id,
        }
    

class ExternalLink(models.Model):
    linking_page = models.CharField(max_length=150)
    linked_page = models.CharField(max_length=150)
    rel = models.CharField(max_length=10)
    is_linked_page_available = models.BooleanField(blank=True, null=True)

    def __str__(self):
        return f'link {self.rel} from {self.linking_page} to {self.linked_page}'


class ExternalLinksManager(models.Model):
    site = models.OneToOneField(Site, on_delete=models.CASCADE, related_name="external_links")
    links = models.ManyToManyField(ExternalLink)
    excluded = models.JSONField(default=list)
    date = models.DateField(auto_now=True)
    progress_current = models.IntegerField(default=0)
    progress_target = models.IntegerField(default=1)