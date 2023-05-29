from django.contrib import admin
from .models import *
from .forms import *

# Register your models here.


class UserRoomAssignAdmin(admin.ModelAdmin):
    form = UserRoomAssignForm
    list_display = ('user', 'room', 'duration', 'remain_duration')
    search_fields = ['room__room_id', 'user__username']
    readonly_fields = ('remain_duration',)

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            obj.room.user.remove(obj.user)
        super().delete_queryset(request=request, queryset=queryset)
        return None


admin.site.register(UserRoomAssign, UserRoomAssignAdmin)
# admin.site.register(UserACAssign)
# admin.site.register(RoomDurationOver)
