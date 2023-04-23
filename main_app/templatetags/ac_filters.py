from django import template
from ..models import AC, Room

register = template.Library()

@register.filter
def rooms_ac(room, user):
    if user.is_admin:
        room = Room.objects.get(room_id=room.room_id)
        return AC.objects.filter(room=room)
    else:
        room = Room.objects.get(room_id=room.room_id)
        return AC.objects.filter(room=room).filter(user=user)
