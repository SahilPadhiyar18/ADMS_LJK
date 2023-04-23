from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('ac_status_change', views.change_ac_status, name='ac_status')
]