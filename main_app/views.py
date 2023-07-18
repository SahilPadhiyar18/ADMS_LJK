from django.shortcuts import render, redirect
from .models import Room, AC
from django.contrib.auth.decorators import login_required
import json
from .utils import *
from django.http import JsonResponse
from django.db.models import F

# Create your views here.

@login_required(login_url='login')
def home(request):
    if request.user.is_admin or request.user.user_type == 2:
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
    try:
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
                if status:
                    make_user_ac_assign_obj(request,  ac)
                else:
                    delete_user_ac_after_off_status(request, ac)

                save_logs_to_db(request, ac, field, status)
                return redirect('home')
            except Exception as e:
                print(e)
                return redirect('home')
    except Exception as e:
        print(f"Exception occur in change_ac_status function: {e}")

   
def acupdate(request):
    try:
        esp_id = request.GET['espid']
        print(esp_id)
        circuit = Circuit.objects.filter(esp_id=esp_id.upper()).exists()
        if circuit:
            if AC.objects.filter(circuit__esp_id=esp_id, no=1).exists():
                ac1 = AC.objects.get(circuit__esp_id=esp_id, no=1)
                ac1.status = bool(int(request.GET['ac1']))
                ac1.ping = timezone.localtime()
                ac1.current = request.GET['ac1cur']
                ac1.save()
            if AC.objects.filter(circuit__esp_id=esp_id, no=2).exists():
                ac2 = AC.objects.get(circuit__esp_id=esp_id, no=2)
                ac2.status = bool(int(request.GET['ac2']))
                ac2.ping = timezone.localtime()
                ac2.current = request.GET['ac2cur']
                ac2.save()
            if AC.objects.filter(circuit__esp_id=esp_id, no=3).exists():
                ac3 = AC.objects.get(circuit__esp_id=esp_id, no=3)
                ac3.status = bool(int(request.GET['ac3']))
                ac3.ping = timezone.localtime()
                ac3.current = request.GET['ac3cur']
                ac3.save()
            print('all acs are updated successfully')
            # return HttpResponse("Please Register your 1")
            return JsonResponse(list(AC.objects.filter(circuit__esp_id=esp_id).values('no', value=F('ac_esp'))), safe=False)
        else:
            return HttpResponse("Please Register your Self")
    except Exception as e:
        # print("PASS")
        return HttpResponse("Error")

