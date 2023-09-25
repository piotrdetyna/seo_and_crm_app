from django.urls import path
from . import views

urlpatterns = [
    path('sites/', views.SiteView.as_view(), name='sites'),
    path('sites/<int:site_id>/', views.SiteView.as_view(), name='site_details'),
    path('sites/<int:site_id>/backlinks/status/', views.check_backlinks_status, name='site_backlinks_status'),
    path('sites/<int:site_id>/external-links/', views.ExternalLinksView.as_view(), name="find_external_links"),
    path('sites/<int:site_id>/<str:attribute>/', views.SiteView.as_view(), name='site_detail'),
    
    path('session/current-site/', views.CurrentSiteView.as_view(), name="current_site"),

    path('clients/', views.ClientView.as_view(), name='clients'),
    path('clients/<int:client_id>/', views.ClientView.as_view(), name='client_details'),
    path('clients/<int:client_id>/<str:attribute>/', views.ClientView.as_view(), name='client_detail'),

    path('notes/', views.NoteView.as_view(), name="notes"), 
    path('notes/<int:note_id>/', views.NoteView.as_view(), name='note_details'),
    path('notes/<int:note_id>/<str:attribute>/', views.NoteView.as_view(), name='note_detail'),

    path('contracts/', views.ContractView.as_view(), name='contracts'),
    path('contracts/<int:contract_id>/', views.ContractView.as_view(), name='contract_details'),
    path('contracts/urgency/', views.check_contracts_urgency, name="contracts_urgency"),
    path('contracts/<int:contract_id>/urgency/', views.check_contracts_urgency, name="contract_urgency"),
    path('contracts/<int:contract_id>/<str:attribute>/', views.ContractView.as_view(), name='contract_detail'),

    path('invoices/', views.InvoiceView.as_view(), name='invoices'),
    path('invoices/<int:invoice_id>/', views.InvoiceView.as_view(), name='invoice_details'),
    path('invoices/<int:invoice_id>/<str:attribute>/', views.InvoiceView.as_view(), name="invoice_detail"),

    path('backlinks/', views.BacklinkView.as_view(), name='backlinks'),
    path('backlinks/<int:backlink_id>/', views.BacklinkView.as_view(), name='backlink_details'),
    path('backlinks/status/', views.check_backlinks_status, name="backlinks_status"),
    path('backlinks/<int:backlink_id>/status/', views.check_backlinks_status, name="backlink_status"),
    path('backlinks/<int:backlink_id>/<str:attribute>/', views.BacklinkView.as_view(), name='backlink_details'),
    
    path('login/', views.login_view, name="login_view"),
    path('logout/', views.logout_view, name="logout_view"),    
]