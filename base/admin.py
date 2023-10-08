from django.contrib import admin
from .models import User, Keyword, Check, Client, Site, Contract, ExternalLinksManager, ExternalLink, Note, Backlink

admin.site.register(User)
admin.site.register(Client)
admin.site.register(Site)
admin.site.register(ExternalLinksManager)
admin.site.register(ExternalLink)
admin.site.register(Note)
admin.site.register(Backlink)
admin.site.register(Contract)
admin.site.register(Keyword)
admin.site.register(Check)