from django.contrib import admin
from .models import User, Client, Site, ExternalLinks

admin.site.register(User)
admin.site.register(Client)
admin.site.register(Site)
admin.site.register(ExternalLinks)