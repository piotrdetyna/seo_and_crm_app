from django.urls import path
from . import views

urlpatterns = [
    path('sites/', views.SiteView.as_view(), name='sites'),
    path('sites/<int:site_id>/', views.SiteView.as_view(), name='site_details'),
    path('sites/current/', views.set_current_site, name="set_current_site"),

    path('clients/', views.ClientView.as_view(), name='clients'),
    path('clients/<int:client_id>/', views.ClientView.as_view(), name='client_details'),

    path('notes/', views.NoteView.as_view(), name="notes"), 
    path('notes/<int:note_id>/', views.NoteView.as_view(), name='note_details'),

    path('contracts/', views.ContractView.as_view(), name='contracts'),
    path('contract/<int:contract_id>/', views.ContractView.as_view(), name='contract_details'),
    path('contracts/urgency/', views.check_contracts_urgency, name="check_contracts_urgency"),

    path('invoices/', views.InvoiceView.as_view(), name='invoices'),
    path('invoices/<int:invoice_id>/', views.InvoiceView.as_view(), name='invoice_details'),
    path('invoice-get-file/<int:invoice_id>/<str:file_type>/', views.invoice_get_file, name="invoice_get_file"),

    path('find-external/<int:site_id>/', views.find_external_links, name="find_external_links"),
    path('check-linked-page-availability/<int:site_id>/', views.check_linked_pages_availability, name="check_linked_pages_availability"),
    path('external-links-progress/<int:site_id>/', views.get_external_links_progress, name="get_external_links_progress"),    
    
    path('login/', views.login_view, name="login_view"),
    path('logout/', views.logout_view, name="logout_view"),

    path('backlinks/', views.BacklinkView.as_view(), name='backlinks'),
    path('backlinks/<int:backlink_id>/', views.BacklinkView.as_view(), name='backlink_details'),
    path('check-backlinks-status/<int:site_id>/', views.check_backlinks_status, name="check_backlinks_status"),
]