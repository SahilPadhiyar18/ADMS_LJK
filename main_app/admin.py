from django.contrib import admin
from .forms import *


class CircuitAdmin(admin.ModelAdmin):
    change_list_template = 'admin/Circuit_change_list.html'
    form = CircuitForm
    list_display = ('panel_id', 'esp_id')
    search_fields = ['esp_id']


class RoomAdmin(admin.ModelAdmin):
    change_list_template = 'admin/Room_change_list.html'
    readonly_fields = ('user',)
    form = RoomForm
    list_display = ('room_id',)
    search_fields = ['room_id']


class ACAdmin(admin.ModelAdmin):
    change_list_template = 'admin/AC_change_list.html'
    readonly_fields = ('no', 'total_ac_working_hours')
    form = ACForm
    list_display = ('name', 'room', 'circuit', 'ac_esp', 'lock', 'total_ac_working_hours')
    search_fields = ['name', 'room__room_id', 'circuit__esp_id']


# Register your models here.
admin.site.register(AC, ACAdmin)
admin.site.register(Circuit, CircuitAdmin)
admin.site.register(Room, RoomAdmin)



