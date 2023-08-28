from django.db import models
from django.contrib.auth.models import AbstractUser
from slugify import slugify

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
    

class ExternalLinks(models.Model):
    site = models.ForeignKey(Site, on_delete=models.CASCADE, related_name="external_links")
    links = models.JSONField()
    excluded = models.JSONField()
    date = models.DateField(auto_now=True)


