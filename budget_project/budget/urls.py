from django.urls import path

from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('add_category/', views.add_category, name='add_category'),
    path('add_transaction/', views.add_transaction, name='add_transaction'),
    path('export_csv/', views.export_csv, name='export_csv'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
