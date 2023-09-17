from django.urls import path, include
from . import views



urlpatterns = [
    path('', views.index, name="index"),
    path('add-site/', views.add_site_form, name="add_site_form"),

    path('external/<int:site_id>/', views.external_links, name="external_links"),
    path('external/', views.external_links, name="external_links"),
    
    path('site/<int:site_id>/', views.site_details, name="site_details"),
    path('site/', views.site_details, name="site_details"),
    
    path('notes/', views.notes, name="notes"),
    path('notes/<int:site_id>', views.notes, name="notes"),

    path('site-choice/', views.site_choice, name="site_choice"),

    path('backlinks/', views.backlinks, name="backlinks"),
    path('backlinks/<int:site_id>', views.backlinks, name="backlinks"),

    path('api/', include('base.api.urls')),
    path('login/', views.login, name='login'),

    path('clients/', views.clients, name="clients"),
    path('client/<int:client_id>/', views.client, name="client"),

    path('contracts/', views.contracts, name="contracts"),
    path('contract/<int:contract_id>/', views.contract, name="contract"),
]

