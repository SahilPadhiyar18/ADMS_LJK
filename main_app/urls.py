from django.urls import path
from . import views
import threading
from .utils import loop_thread

urlpatterns = [
    path('', views.home, name='home'),
    path('ac_status_change', views.change_ac_status, name='ac_status')
]


thread_one = threading.Thread(target=loop_thread)

thread_one.daemon = True

thread_one.start()