from django.urls import path
from . import views
import threading
from .utils import loop_thread
from .save_excel_data_functions import *

urlpatterns = [
    path('', views.home, name='home'),
    path('ac_status_change', views.change_ac_status, name='ac_status'),

    path('acupdate', views.acupdate, name='acupdate'),

    # urls for save data from excel file to db
    path('room-data', save_room_data_db, name='room-data'),
    path('circuit-data', save_circuit_data_db, name='circuit-data'),
    path('ac-data', save_ac_data_db, name='ac-data'),
    path('user-data', save_user_data_db, name='user-data'),
    path('user-room-assign-data', save_user_room_assign_data_db, name='user-room-assign-data')

]


# thread_one = threading.Thread(target=loop_thread)

# thread_one.daemon = True

# thread_one.start()
