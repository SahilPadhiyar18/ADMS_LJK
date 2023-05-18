from django.shortcuts import render, redirect
from .models import Room, AC
from django.contrib.auth.decorators import login_required
import json
from .utils import save_logs_to_db

# Create your views here.

@login_required(login_url='login')
def home(request):
    if request.user.is_admin:
        room_data = Room.objects.all()
    else:
        room_data = Room.objects.filter(user=request.user)    
        
    ac_data = AC.objects.all()
    context = {
        'rooms': room_data,
        'acs': ac_data
    } 
    return render(request, 'main_templates/home.html', context)


@login_required(login_url='login')
def change_ac_status(request):
    if request.method == 'GET':
        try:
            ac_uuid = request.GET.get('ac_uuid')
            field = request.GET.get('field')
            status = json.loads(request.GET.get('status'))
            ac = AC.objects.get(ac_uuid=ac_uuid)
            if field == 'ac_esp':
                ac.ac_esp = status
            elif field == 'ac_lock':
                ac.lock = status
            ac.save()
            save_logs_to_db(request, ac, field, status)
            return redirect('home')
        except Exception as e:
            print(e)
            return redirect('home')
        
def get_acs_of_room(request, room_id):
    room = Room.objects.get(room_id=room.room_id, user=request.user)
    acs =  AC.objects.filter(room=room).order_by('created_at')
    acs_json = {}
    for ac in acs:
        acs_json[ac.name] = {
            'uuid': ac.ac_uuid.urn[9:],
            'room': ac.room.room_id,
            'circuit': ac.circuit.esp_id,
            'ac_esp': ac.ac_esp,
            'lock': ac.lock,
            'ping': ac.ping.strftime('%Y-%m-%d %H:%M:%S'),
            'status': ac.status,
            'created_at': ac.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': ac.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        }
    final_json = json.dumps(acs_json)
    
    return final_json    