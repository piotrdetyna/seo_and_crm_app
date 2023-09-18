from django.db import models
from django.contrib.auth.models import AbstractUser
from slugify import slugify
from django.core.exceptions import ValidationError, ObjectDoesNotExist 
from django.core.files.storage import FileSystemStorage
from crm.settings import PRIVATE_STORAGE_ROOT, MEDIA_ROOT
from django.dispatch import receiver
import os

private_storage = FileSystemStorage(location=PRIVATE_STORAGE_ROOT)



def logo_file_name(instance, filename):
    return '/'.join(['sites', str(instance.id), 'logo.'+ filename.split('.')[-1]])


def pdf_upload_to(instance, filename):
    return '/'.join(['clients', str(instance.contract.client.id), 'invoices', str(instance.contract.id), str(instance.id) ])


class User(AbstractUser):
    pass



class OverwriteStorage(FileSystemStorage):
    def get_available_name(self, name, max_length=None):
        # If the filename already exists, remove it as if it was a true file system
        if self.exists(name):
            os.remove(os.path.join(MEDIA_ROOT, name))
        return name


class Client(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)

    is_company = models.BooleanField()
    nip = models.CharField(max_length=10, blank=True)
    address = models.CharField(max_length=200, blank=True)
    full_name = models.CharField(max_length=200, blank=True)

    def clean(self):
        #when client is a company
        if self.is_company:
            if not self.nip:
                raise ValidationError('If client is a company, "nip" field must be filled.')
        #when client is a private person
        else:
            if not self.address or not self.full_name:
                raise ValidationError("If client is a private person, both 'address' and 'full_name' must be filled.")

    def save(self, *args, **kwargs):
        self.clean()
        super(Client, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Site(models.Model):
    url = models.CharField(max_length=150, unique=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="sites")
    logo = models.ImageField(upload_to=logo_file_name, storage=OverwriteStorage, blank=True, null=True)
    date = models.DateField(auto_now_add=True)

    #save object firstly without logo, and with logo at the second time to get object id after first save 
    def save(self, *args, **kwargs):
        if not self.id and self.logo:
            logo_tmp = self.logo
            self.logo = None
            super(Site, self).save(*args, **kwargs)
            self.logo = logo_tmp
            self.save()
        else:
            super(Site, self).save(*args, **kwargs)

    def __str__(self):
        return self.url
    
    
@receiver(models.signals.post_delete, sender=Site)
def auto_delete_file_on_delete(sender, instance, **kwargs):

    if instance.logo:
        if os.path.isfile(instance.logo.path):
            os.remove(instance.logo.path)


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
    text = models.CharField(max_length=10_000)
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
    


class Contract(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="contracts")
    site = models.ForeignKey(Site, on_delete=models.CASCADE, related_name="contracts")
    payment_frequency = models.IntegerField()
    payment_date = models.DateField()
    value = models.IntegerField()

    CATEGORIES = (
        ('seo', 'Pozycjonowanie'),
        ('hosting', 'Hosting'),
        ('domain', 'Domena'),
        ('site_care', 'Opieka nad stroną'),
        ('other', 'Inne'),
    )
    category = models.CharField(max_length=9, choices=CATEGORIES)

    def clean(self):
        # Ensure that the site is associated with the same client
        if self.site.client != self.client:
            raise ValidationError("The site must belong to the same client as the contract.")

    def save(self, *args, **kwargs):
        try:
            old_contract = Contract.objects.get(id=self.id)
            if old_contract.site_id != self.site_id:
                self.client = self.site.client
        except ObjectDoesNotExist:
            if not self.client_id:
                self.client = self.site.client
        self.full_clean()
        super(Contract, self).save(*args, **kwargs)


class Invoice(models.Model):
    contract = models.OneToOneField(Contract, on_delete=models.CASCADE, related_name="invoices")
    pdf = models.FileField(upload_to=pdf_upload_to, blank=True)
    date = models.DateField(auto_now_add=True)
    update_date = models.DateField(auto_now=True)
    