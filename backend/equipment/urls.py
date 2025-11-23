from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('upload/', views.upload_csv, name='upload_csv'),
    path('summary/', views.get_summary, name='get_summary'),
    path('summary/<int:dataset_id>/', views.get_summary, name='get_summary_by_id'),
    path('history/', views.get_history, name='get_history'),
    path('dataset/<int:dataset_id>/', views.get_dataset_data, name='get_dataset_data'),
    path('dataset/<int:dataset_id>/pdf/', views.generate_pdf_report, name='generate_pdf'),
]












