from django.urls import path
from . import views

app_name = 'donors'

urlpatterns = [
    path('donor/', views.donor_register, name='donor'),
    path('receiver/', views.receiver_request, name='receiver'),
    path('list/', views.list_donors, name='list_donors'),
    path('requests/', views.list_blood_requests, name='list_requests'),
    path('requests/urgent/', views.urgent_requests, name='urgent_requests'),
]
