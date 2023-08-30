from django.contrib import admin
from .models import User, Client, Site, ExternalLinksManager, ExternalLink

admin.site.register(User)
admin.site.register(Client)
admin.site.register(Site)
admin.site.register(ExternalLinksManager)
admin.site.register(ExternalLink)