from django import template
from ..models import AC, Room
from user_assign_duration.models import *

register = template.Library()

@register.filter
def rooms_ac(room, user):
    if user.is_admin or user.user_type == 2:
        room = Room.objects.get(room_id=room.room_id)
        return AC.objects.filter(room=room).order_by('created_at')
    else:
        room = Room.objects.get(room_id=room.room_id, user=user)
        return AC.objects.filter(room=room).order_by('created_at')

@register.filter
def room_color(room, user):
    try:
        room_assign_over_exists = RoomDurationOver.objects.filter(user=user, room=room).exists()
        if room_assign_over_exists:
            room_assign_over = RoomDurationOver.objects.get(user=user, room=room)
            status = room_assign_over.is_time_over
            return status
    except Exception as e:
        print(e)

@register.filter
def get_remain_time(room, user):
    try:
        user_room_assign = UserRoomAssign.objects.get(user=user, room=room)
        remain_duration = user_room_assign.remain_duration
        duration = remain_duration - datetime.timedelta(microseconds=remain_duration.microseconds)
        return duration
    except Exception as e:
        print(e)


@register.filter
def get_ping_status(ping):
    current_time = timezone.localtime()
    if ping and current_time - timezone.localtime(ping) <= datetime.timedelta(minutes=2):
        status = 'Online'
    else:
        status = 'Offline'
    return status