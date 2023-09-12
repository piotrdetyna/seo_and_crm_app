from django.urls import path
from . import views

urlpatterns = [
    path('add-site/', views.add_site, name="add_site"),
    path('edit-site/', views.edit_site, name="edit_site"),
    path('delete-site/', views.delete_site, name="delete_site"),
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
    path('login/', views.login_view, name="login_view"),
    path('logout/', views.logout_view, name="logout_view"),
    path('add-backlink/', views.add_backlink, name="add_backlink"),
    path('delete-backlink/', views.delete_backlink, name="delete_backlink"),
    path('check-backlinks-status/', views.check_backlinks_status, name="check_backlinks_status"),
]