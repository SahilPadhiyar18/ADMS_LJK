from django.contrib import admin
from .models import *
from .forms import *

# Register your models here.


class UserRoomAssignAdmin(admin.ModelAdmin):
    form = UserRoomAssignForm
    list_display = ('room', 'duration')
    search_fields = ['room__room_id', 'user__username']


admin.site.register(UserRoomAssign, UserRoomAssignAdmin)
# admin.site.register(UserACAssign)
# admin.site.register(RoomDurationOver)
