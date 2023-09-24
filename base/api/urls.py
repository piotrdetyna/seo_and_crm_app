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


    path('find-external/<int:site_id>/', views.find_external_links, name="find_external_links"),
    path('check-linked-page-availability/<int:site_id>/', views.check_linked_pages_availability, name="check_linked_pages_availability"),
    path('external-links-progress/<int:site_id>/', views.get_external_links_progress, name="get_external_links_progress"),

    
    
    path('login/', views.login_view, name="login_view"),
    path('logout/', views.logout_view, name="logout_view"),

    path('add-backlink/', views.add_backlink, name="add_backlink"),
    path('delete-backlink/<int:backlink_id>/', views.delete_backlink, name="delete_backlink"),
    path('check-backlinks-status/<int:site_id>/', views.check_backlinks_status, name="check_backlinks_status"),

    path('add-contract/', views.add_contract, name="add_contract"),
    path('delete-contract/<int:contract_id>/', views.delete_contract, name="delete_contract"),
    path('edit-contract/<int:contract_id>/', views.edit_contract, name="edit_contract"),
    path('check-contracts-urgency/', views.check_contracts_urgency, name="check_contracts_urgency"),

    path('add-invoice/', views.add_invoice, name="add_invoice"),
    path('edit-invoice/<int:invoice_id>/', views.edit_invoice, name="edit_invoice"),
    path('delete-invoice/<int:invoice_id>/', views.delete_invoice, name="delete_invoice"),
    

    path('invoice-get-file/<int:invoice_id>/<str:file_type>/', views.invoice_get_file, name="invoice_get_file"),
]