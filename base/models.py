from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError 
from django.core.files.storage import FileSystemStorage
from crm.settings import PRIVATE_STORAGE_ROOT, MEDIA_ROOT
from django.dispatch import receiver
import os
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import date, timedelta

private_storage = FileSystemStorage(location=PRIVATE_STORAGE_ROOT)



def logo_file_name(instance, filename):
    return '/'.join(['sites', str(instance.id), 'logo.'+ filename.split('.')[-1]])


def invoice_upload_to(instance, filename):
    return '/'.join(['clients', str(instance.contract.site.client.id), 'contracts', str(instance.contract.id), 'invoices', filename ])


def report_upload_to(instance, filename):
    return '/'.join(['clients', str(instance.contract.site.client.id), 'contracts', str(instance.contract.id), 'reports', filename ])

class User(AbstractUser):
    pass


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


class ExternalLink(models.Model):
    manager = models.ForeignKey('ExternalLinksManager', related_name='external_links', on_delete=models.CASCADE)
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
    site = models.OneToOneField('Site', on_delete=models.CASCADE, related_name="external_links_manager")
    excluded = models.JSONField(default=list, blank=True)
    date = models.DateField(auto_now=True)
    progress_current = models.IntegerField(default=0)
    progress_target = models.IntegerField(default=1)

    def update(self, **kwargs):
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        self.save()

    def delete_links(self):
        self.external_links.all().delete()
        self.save()
    
    def clear_progress(self):
        self.progress_current = 0
        self.progress_target = 1
        self.save()

    def get_unique_linked_pages(self):
        unique_linked_pages = set()
        for external_link in self.external_links.all():
            unique_linked_pages.add(external_link.linked_page)
        return unique_linked_pages
    
    def increase_progress(self):
        self.progress_current += 1
        self.save()


class Site(models.Model):
    url = models.CharField(max_length=150, unique=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="sites")
    logo = models.ImageField(upload_to=logo_file_name, default='default.jpg')
    date = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['-id']

    
    def save(self, *args, **kwargs):
        new_site = not self.id            
        #save object firstly without logo, and with logo at the second time to get object id after first save 
        if new_site and self.logo:
            
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


class Note(models.Model):
    text = models.CharField(max_length=10_000, blank=True)
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

    class Meta:
        ordering = ['-rel_changed', '-status_changed']

    def __str__(self):
        return f'Backlink from {self.linking_page} to {self.site.url}'
    


class Contract(models.Model):
    site = models.ForeignKey(Site, on_delete=models.CASCADE, related_name="contracts")
    invoice_frequency = models.IntegerField()
    invoice_date = models.DateField()
    days_before_invoice_date_to_mark_urgent = models.IntegerField(
        default=0, 
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    is_urgent = models.BooleanField(default=False)
    value = models.IntegerField()

    CATEGORIES = (
        ('seo', 'Pozycjonowanie'),
        ('hosting', 'Hosting'),
        ('domain', 'Domena'),
        ('site_care', 'Opieka nad stroną'),
        ('other', 'Inne'),
    )
    category = models.CharField(max_length=9, choices=CATEGORIES)

    class Meta:
        ordering = ['-is_urgent', 'invoice_date']

    def check_urgency(self):
        self.is_urgent = False
        if self.invoice_date - timedelta(days=self.days_before_invoice_date_to_mark_urgent) <= date.today():
            self.is_urgent = True
        self.save()



def validate_pdf_file_extension(value):
    if not value.name.endswith('.pdf'):
        raise ValidationError("Submitted file must have 'pdf' extension")

def validate_file_size(value):
    max_file_size = 5 * 1024 * 1024  # 5MB
    if value.size > max_file_size:
        raise ValidationError(f"Submitted file is too big. Max valid size is {max_file_size / (1024 * 1024)}MB")


class Invoice(models.Model):
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, related_name="invoices")
    is_paid = models.BooleanField(default=False)
    invoice_file = models.FileField(
        upload_to=invoice_upload_to, 
        storage=private_storage, 
        validators=[validate_pdf_file_extension, validate_file_size]
    )
    report_file = models.FileField(
        upload_to=report_upload_to, 
        storage=private_storage, 
        validators=[validate_pdf_file_extension, validate_file_size],
        blank=True,
        null=True,
    )
    payment_date = models.DateField()
    date = models.DateField(auto_now_add=True)
    update_date = models.DateField(auto_now=True)

    class Meta:
        ordering = ['-is_paid', 'date']