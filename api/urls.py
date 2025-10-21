from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    # Folder endpoints
    path('folders/', views.folder_list, name='folder_list'),
    path('folders/<int:folder_id>/', views.folder_detail, name='folder_detail'),

    # Document endpoints
    path('documents/', views.document_list, name='document_list'),
    path('documents/<int:document_id>/', views.document_detail, name='document_detail'),
    path('documents/<int:document_id>/download/', views.document_download, name='document_download'),
]
