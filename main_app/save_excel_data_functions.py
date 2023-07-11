from django.shortcuts import redirect
from .forms import *
from django.template.response import TemplateResponse
import pandas as pd
from user_assign_duration.models import *
from datetime import datetime, timedelta

def save_room_data_db(request):
    if request.method == 'POST':
        form = UploadExcelForm(request.POST, request.FILES)
        if form.is_valid():
            excel_file = form.cleaned_data['excel_file']
            room_data = pd.read_excel(excel_file)
            for index, row in room_data.iterrows():
                try:
                    room_id = str(row['room_id']).split('.')[0] if row['room_id'] else None

                    if room_id and room_id != 'room_id' and room_id != 'nan':
                        room = Room(room_id=room_id)
                        room.save()
                except Exception as e:
                    print(f'Exception occur in save_room_data_db function: {e}')

            return redirect('admin:index')
    else:
        form = UploadExcelForm()

    context = {
        'form': form,
    }
    return TemplateResponse(request, 'admin/upload_excel.html', context)


def save_circuit_data_db(request):
    if request.method == 'POST':
        form = UploadExcelForm(request.POST, request.FILES)
        if form.is_valid():
            excel_file = form.cleaned_data['excel_file']
            circuit_data = pd.read_excel(excel_file)
            for index, row in circuit_data.iterrows():
                try:
                    panel_id = str(row['panel_id']).split('.')[0] if row['panel_id'] else None
                    esp_id = str(row['esp_id']).split('.')[0] if row['esp_id'] else None

                    if (panel_id and panel_id != 'panel_id' and panel_id != 'nan') and (esp_id and esp_id != 'esp_id' and esp_id != 'nan'):
                        circuit = Circuit(panel_id=panel_id, esp_id=esp_id)
                        circuit.save()
                except Exception as e:
                    print(f'Exception occur in save_circuit_data_db function: {e}')
            return redirect('admin:index')
    else:
        form = UploadExcelForm()

    context = {
        'form': form,
    }
    return TemplateResponse(request, 'admin/upload_excel.html', context)


def save_ac_data_db(request):
    if request.method == 'POST':
        form = UploadExcelForm(request.POST, request.FILES)
        if form.is_valid():
            excel_file = form.cleaned_data['excel_file']
            ac_data = pd.read_excel(excel_file)
            for index, row in ac_data.iterrows():
                try:
                    room = str(row['room']).split('.')[0].upper() if row['room'] else None
                    circuit = str(row['circuit']).split('.')[0].upper() if row['circuit'] else None
                    name = str(row['name']).split('.')[0] if row['name'] else None
                    no = str(row['no']).split('.')[0] if row['no'] else None

                    if (room and room != 'room' and room != 'nan' and room != 'NAN') and (
                            circuit and circuit != 'circuit' and circuit != 'nan' and circuit != 'NAN') and (
                             name and name != 'name' and name != 'nan') and (no and no != 'no' and no != 'nan' and room != 'NAN'):

                        room_obj, circuit_obj = None, None

                        if Room.objects.filter(room_id=room).exists():
                            room_obj = Room.objects.get(room_id=room)
                        if Circuit.objects.filter(esp_id=circuit).exists():
                            circuit_obj = Circuit.objects.get(esp_id=circuit)

                        if room_obj and circuit_obj and name:
                            ac = AC(room=room_obj, circuit=circuit_obj, name=name, no=int(no))
                            ac.save()

                except Exception as e:
                    print(f'Exception occur in save_circuit_data_db function: {e}')
            return redirect('admin:index')
    else:
        form = UploadExcelForm()

    context = {
        'form': form,
    }
    return TemplateResponse(request, 'admin/upload_excel.html', context)


def save_user_room_assign_data_db(request):
    if request.method == 'POST':
        form = UploadExcelForm(request.POST, request.FILES)
        if form.is_valid():
            excel_file = form.cleaned_data['excel_file']
            ac_data = pd.read_excel(excel_file)
            for index, row in ac_data.iterrows():
                try:
                    user = str(row['user']).split('.')[0] if row['user'] else None
                    room = str(row['room']).split('.')[0].upper() if row['room'] else None
                    duration = str(row['duration']).split('.')[0] if row['duration'] else None

                    if (room and room != 'room' and room != 'nan' and room != 'NAN') and (
                            user and user != 'user' and user != 'nan') and (
                            duration and duration != 'duration' and duration != 'nan'):

                        room_obj, user_obj = None, None

                        if Room.objects.filter(room_id=room).exists():
                            room_obj = Room.objects.get(room_id=room)
                        if User.objects.filter(username=user).exists():
                            user_obj = User.objects.get(username=user)

                        duration_field = get_duration_format(duration)

                        if room_obj and user_obj and duration:
                            user_room_assign = UserRoomAssign(user=user_obj, room=room_obj, duration=duration_field)
                            is_created_obj = checked_room_assign_obj(user_obj, room_obj, duration)
                            if is_created_obj:
                                user_room_assign.save()

                except Exception as e:
                    print(f'Exception occur in save_circuit_data_db function: {e}')
            return redirect('admin:index')
    else:
        form = UploadExcelForm()

    context = {
        'form': form,
    }
    return TemplateResponse(request, 'admin/upload_excel.html', context)


def save_user_data_db(request):
    if request.method == 'POST':
        form = UploadExcelForm(request.POST, request.FILES)
        if form.is_valid():
            excel_file = form.cleaned_data['excel_file']
            user_data = pd.read_excel(excel_file)
            for index, row in user_data.iterrows():
                try:
                    username = str(row['username']).split('.')[0] if row['username'] else None
                    email = str(row['email']) if row['email'] else None
                    password = str(row['password']).split('.')[0] if row['password'] else None

                    if (username and username != 'username' and username != 'nan') and (
                            email and email != 'email' and email != 'nan') and (
                               password and password != 'password' and password != 'nan'):
                        user = User(username=username, email=email, password=password)
                        user.save()

                except Exception as e:
                    print(f'Exception occur in save_circuit_data_db function: {e}')
            return redirect('admin:index')
    else:
        form = UploadExcelForm()

    context = {
        'form': form,
    }
    return TemplateResponse(request, 'admin/upload_excel.html', context)


def get_duration_format(duration_str):
    duration = datetime.strptime(duration_str, '%H:%M:%S')
    duration = timedelta(hours=duration.hour, minutes=duration.minute, seconds=duration.second)
    return duration


def checked_room_assign_obj(user, room, duration):
    is_created_obj = False
    if not user:
        return is_created_obj
    elif room is None:
        return is_created_obj
    elif duration is None:
        return is_created_obj

    elif room and duration and user:
        if user.is_admin:
            return is_created_obj
        if UserRoomAssign.objects.filter(room=room, user=user):
            for user_room in UserRoomAssign.objects.filter(room=room, user=user):
                user_room.delete()

        if not user.is_admin:
            room_duration_over = RoomDurationOver.objects.filter(user=user, room=room)
            if room_duration_over:
                for room_dur_obj in room_duration_over:
                    room_dur_obj.delete()

            new_room_duration_over = RoomDurationOver(user=user, room=room, duration=duration, remain_duration=duration,
                                                      is_time_over=False)
            new_room_duration_over.save()

            is_created_obj = True

        room.user.add(user)

        return is_created_obj