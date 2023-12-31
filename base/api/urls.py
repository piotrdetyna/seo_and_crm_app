from django.urls import path
from . import views

urlpatterns = [
    path('sites/', views.SiteView.as_view(), name='sites'),
    path('sites/expiry/', views.check_domain_expiry, name='sites_expiry_dates'),
    path('sites/<int:site_id>/', views.SiteView.as_view(), name='site_details'),
    path('sites/<int:site_id>/expiry/', views.check_domain_expiry, name='site_expiry_date'),
    
    path('session/current-site/', views.CurrentSiteView.as_view(), name="current_site"),
    path('session/login/', views.login_view, name="login_view"), 
    path('session/logout/', views.logout_view, name="logout_view"),    

    path('clients/', views.ClientView.as_view(), name='clients'),
    path('clients/<int:client_id>/', views.ClientView.as_view(), name='client_details'),

    path('notes/', views.NoteView.as_view(), name="notes"), 
    path('notes/<int:note_id>/', views.NoteView.as_view(), name='note_details'),

    path('contracts/', views.ContractView.as_view(), name='contracts'),
    path('contracts/<int:contract_id>/', views.ContractView.as_view(), name='contract_details'),
    path('contracts/urgency/', views.check_contracts_urgency, name="contracts_urgency"),
    path('contracts/<int:contract_id>/urgency/', views.check_contracts_urgency, name="contract_urgency"),

    path('invoices/', views.InvoiceView.as_view(), name='invoices'),
    path('invoices/<int:invoice_id>/', views.InvoiceView.as_view(), name='invoice_details'),
    path('invoices/overduity/', views.update_invoice_overduity, name='invoices_overduity'),
    path('invoices/<int:invoice_id>/overduity/', views.update_invoice_overduity, name='invoice_overduity'),

    path('backlinks/', views.BacklinkView.as_view(), name='backlinks'),
    path('backlinks/<int:backlink_id>/', views.BacklinkView.as_view(), name='backlink_details'),
    path('backlinks/status/', views.update_backlinks_status_view, name="backlinks_status"),
    path('backlinks/<int:backlink_id>/status/', views.update_backlinks_status_view, name="backlink_status"),

    path('external-links-managers/', views.ExternalLinksManagersView.as_view(), name="external_links"),
    path('external-links-managers/<int:site_id>/', views.ExternalLinksManagersView.as_view(), name="external_link"),
    path('external-links-managers/status/', views.update_external_links_status_view, name="external_links_status"),
    path('external-links-managers/<int:site_id>/status/', views.update_external_links_status_view, name="external_link_status"),
    
    path('keywords/', views.KeywordView.as_view(), name='keywords'),
    path('keywords/<int:keyword_id>/', views.KeywordView.as_view(), name='keyword_details'),
    path('keywords/position/', views.check_keyword_position, name="keywords_status"),
    path('keywords/<int:keyword_id>/position/', views.check_keyword_position, name="keyword_position"),
]