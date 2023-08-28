from django.contrib import admin
from .models import User, Client, Site, ExternalLinks, ExternalLink

admin.site.register(User)
admin.site.register(Client)
admin.site.register(Site)
admin.site.register(ExternalLinks)
admin.site.register(ExternalLink)