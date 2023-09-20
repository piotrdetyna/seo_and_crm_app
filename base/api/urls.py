from django.urls import path
from . import views

urlpatterns = [
    path('add-site/', views.add_site, name="add_site"),
    path('edit-site/<int:site_id>/', views.edit_site, name="edit_site"),
    path('delete-site/<int:site_id>/', views.delete_site, name="delete_site"),
    path('set-current-site/<int:site_id>', views.set_current_site, name="set_current_site"),
    path('get-sites/', views.get_sites, name="get_sites"),
    path('get-sites/<int:site_id>/', views.get_sites, name="get_sites"),


    path('add-client/', views.add_client, name="add_client"),
    path('edit-client/<int:client_id>/', views.edit_client, name="edit_client"),
    path('delete-client/<int:client_id>/', views.delete_client, name="delete_client"),

    path('find-external/<int:site_id>/', views.find_external_links, name="find_external_links"),
    path('check-linked-page-availability/<int:site_id>/', views.check_linked_pages_availability, name="check_linked_pages_availability"),
    path('external-links-progress/<int:site_id>/', views.get_external_links_progress, name="get_external_links_progress"),
    path('add-note/', views.add_note, name="add_note"), 
    path('get-note/<int:note_id>/', views.get_note, name="get_note"), 
    path('update-note/', views.update_note, name="update_note"),
    path('delete-note/', views.delete_note, name="delete_note"),
    path('login/', views.login_view, name="login_view"),
    path('logout/', views.logout_view, name="logout_view"),
    path('add-backlink/', views.add_backlink, name="add_backlink"),
    path('delete-backlink/', views.delete_backlink, name="delete_backlink"),
    path('check-backlinks-status/', views.check_backlinks_status, name="check_backlinks_status"),

    path('add-contract/', views.add_contract, name="add_contract"),
    path('delete-contract/<int:contract_id>/', views.delete_contract, name="delete_contract"),
    path('edit-contract/<int:contract_id>/', views.edit_contract, name="edit_contract"),
    path('check-contracts-urgency/', views.check_contracts_urgency, name="check_contracts_urgency"),

    path('add-invoice/', views.add_invoice, name="add_invoice"),
    path('delete-invoice/<int:invoice_id>', views.delete_invoice, name="delete_invoice"),
    path('change-invoice-is-paid/<int:invoice_id>/', views.change_invoice_is_paid, name="change_invoice_is_paid"),
    


]