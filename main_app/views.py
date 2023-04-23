from django.shortcuts import render, redirect
from .models import Room, AC
from django.contrib.auth.decorators import login_required
import json
# Create your views here.

@login_required(login_url='login')
def home(request):
    room_data = Room.objects.all()
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
            return redirect('home')
        except Exception as e:
            print(e)
            return redirect('home')
