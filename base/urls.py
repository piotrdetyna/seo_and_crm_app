from django.urls import path, include
from . import views

api_url_patterns = [
    path('add-site/', views.add_site, name="add_site"),
    path('edit-site/', views.edit_site, name="edit_site"),
    path('add-client/', views.add_client, name="add_client"),
    path('find-external/', views.find_external_links, name="find_external_links"),
    path('get-sites/', views.get_sites, name="get_sites"),
    path('get-sites/<int:site_id>/', views.get_sites, name="get_sites"),
    path('set-current-site/', views.set_current_site, name="set_current_site"),
    path('check-linked-page-availability/', views.check_linked_pages_availability, name="check_linked_pages_availability"),
    path('external-links-progress/<int:pk>/', views.get_external_links_progress, name="get_external_links_progress"),
    path('add-note/', views.add_note, name="add_note"), 
    path('get-note/<int:note_id>/', views.get_note, name="get_note"), 
    path('update-note/', views.update_note, name="update_note"),
    path('delete-note/', views.delete_note, name="delete_note"),
    path('site-choice/', views.site_choice, name="site_choice"),
]

urlpatterns = [
    path('', views.index, name="index"),
    path('add-site/', views.add_site_form, name="add_site_form"),

    path('external/<int:site_id>/', views.external_links, name="external_links"),
    path('external/', views.external_links, name="external_links"),
    
    path('site/<int:site_id>/', views.site_details, name="site_details"),
    path('site/', views.site_details, name="site_details"),
    
    path('notes/', views.notes, name="notes"),
    path('notes/<int:site_id>', views.notes, name="notes"),

    path('api/', include(api_url_patterns))
]

