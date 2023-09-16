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


class ExternalLink(models.Model):
    linking_page = models.CharField(max_length=150)
    linked_page = models.CharField(max_length=150)
    rel = models.CharField(max_length=10)
    is_linked_page_available = models.BooleanField(blank=True, null=True)

    def __str__(self):
        return f'link {self.rel} from {self.linking_page} to {self.linked_page}'

    def update(self, **kwargs):
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        self.save()


class ExternalLinksManager(models.Model):
    site = models.OneToOneField(Site, on_delete=models.CASCADE, related_name="external_links")
    links = models.ManyToManyField(ExternalLink)
    excluded = models.JSONField(default=list)
    date = models.DateField(auto_now=True)
    progress_current = models.IntegerField(default=0)
    progress_target = models.IntegerField(default=1)

    def update(self, **kwargs):
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        self.save()

    def delete_links(self):
        self.links.all().delete()
        self.save()
    
    def clear_progress(self):
        self.progress_current = 0
        self.progress_target = 1
        self.save()

    def get_unique_linked_pages(self):
        unique_linked_pages = set()
        for external_link in self.links.all():
            unique_linked_pages.add(external_link.linked_page)
        return unique_linked_pages
    
    def increase_progress(self):
        self.progress_current += 1
        self.save()
        


class Note(models.Model):
    text = models.CharField(max_length=1000)
    site = models.ForeignKey(Site, on_delete=models.CASCADE, related_name='notes')
    date = models.DateField(auto_now_add=True)
    title = models.CharField(max_length=100)



class Backlink(models.Model):
    site = models.ForeignKey(Site, on_delete=models.CASCADE, related_name='backlinks')
    linking_page = models.CharField(max_length=150)
    active = models.BooleanField(blank=True, null=True)
    rel = models.CharField(max_length=10, blank=True, null=True)

    rel_changed = models.BooleanField(default=False)
    status_changed = models.BooleanField(default=False)

    def __str__(self):
        return f'Backlink from {self.linking_page} to {self.site.url}'
