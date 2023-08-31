from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('external/<int:site_id>/', views.external_links, name="external_links"),
    path('external/', views.external_links, name="external_links"),
    path('add-site/', views.add_site, name="add_site"),
    path('site/<int:site_id>/', views.site_details, name="site_details"),
    path('site/', views.site_details, name="site_details"),
    path('edit-site/', views.edit_site, name="edit_site"),
    path('add-client/', views.add_client, name="add_client"),
    path('find-external/', views.find_external_links, name="find_external_links"),
    path('get-sites/', views.get_sites, name="get_sites"),
    path('get-sites/<int:site_id>/', views.get_sites, name="get_sites"),
    path('set-current-site/', views.set_current_site, name="set_current_site"),
    path('check-linked-page-availability/', views.check_linked_page_availability, name="check_linked_page_availability"),
    path('find-external-progress/<int:pk>/', views.get_find_external_links_progress, name="get_find_external_links_progress"),
]