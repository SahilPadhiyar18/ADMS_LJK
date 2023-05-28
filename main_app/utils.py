import time

from adms_logs.models import Logs
from user_assign_duration.models import *
import datetime


def save_logs_to_db(request, ac, field, status):
    try:
        log_exist = False
        task_perform = False
        
        if field == 'ac_esp':
            log = Logs.objects.filter(ac_name=ac.name).filter(task='ON/OFF').filter(on_time__isnull=False).filter(on_by__isnull=False). \
            filter(off_time__isnull=True).filter(off_by__isnull=True).last()
        elif field == 'ac_lock':
            log = Logs.objects.filter(ac_name=ac.name).filter(task='LOCK').filter(on_time__isnull=False).filter(on_by__isnull=False). \
            filter(off_time__isnull=True).filter(off_by__isnull=True).last()

        if log:
            log_exist = True
        else:
            log = Logs()   

        ac_name = ac.name
        log.ac_name = ac_name

        if status:
            on_by = request.user.username
            on_time = ac.get_updated_at_time()
            log.on_by = on_by
            log.on_time = on_time
            log.status = 'ON'
            task_perform = True
        elif log_exist and status is False:
            off_by = request.user.username
            off_time = ac.get_updated_at_time()
            log.off_by = off_by
            log.off_time = off_time
            log.status = 'OFF'
            task_perform = True

        if log_exist and field == 'ac_esp' and task_perform:
            total_on_time = off_time - log.on_time
            log.total_on_time = total_on_time

        if field == 'ac_esp' and task_perform:
            log.task = 'ON/OFF'

            total_ac_working_hours = ac.total_ac_working_hours

            if log_exist:
                if total_ac_working_hours:
                    total_ac_working_hours = total_ac_working_hours + total_on_time
                    log.total_ac_working_hours = total_ac_working_hours
                else:
                    total_ac_working_hours = total_on_time
                    log.total_ac_working_hours = total_ac_working_hours
            else:
                log.total_ac_working_hours = total_ac_working_hours

            ac.total_ac_working_hours = total_ac_working_hours
            ac.save()

        elif field == 'ac_lock' and task_perform:
            log.task = 'LOCK'    
        
        if task_perform:
            log.save()

        print('log successfully added/updated')
    except Exception as e:
        print(f'getting log related errror {e} can not add/update log for {ac.name}')
        print(f"Exception in save_logs_to_db function: {e}")


def make_user_ac_assign_obj(request, ac):
    try:
        user = request.user
        if not user.is_admin:
            room = ac.room
            duration = None
            startTime = timezone.localtime()
            endTime = timezone.localtime()
            useracassign = UserACAssign(user=user, room=room, ac=ac, duration=duration, startTime=startTime, endTime=endTime)
            useracassign.save()
    except Exception as e:
        print(f"Exception in make_user_ac_assign_obj function: {e}")


def delete_user_ac_after_off_status(ac):
    try:
        ac_assign_obj = UserACAssign.objects.filter(ac=ac).exists()

        if ac_assign_obj:
            ac_assign_obj = UserACAssign.objects.get(ac=ac)

            try:
                room_assign = UserRoomAssign.objects.get(user=ac_assign_obj.user, room=ac_assign_obj.room)
                room_duration_over = RoomDurationOver.objects.filter(room=room_assign.room,
                                                                     duration=room_assign.duration,
                                                                     is_time_over=False).exists()
                if room_duration_over:
                    room_duration_over = RoomDurationOver.objects.get(room=room_assign.room,
                                                                         duration=room_assign.duration,
                                                                         is_time_over=False)
                    room_duration_over.remain_duration = room_duration_over.remain_duration - (ac_assign_obj.get_endTime() - ac_assign_obj.get_startTime())
                    room_duration_over.save()
            except Exception as e:
                print(f"Exception in delete_user_ac_after_off_status function: {e}")

            ac_assign_obj.delete()

    except Exception as e:
        print(f"Exception in delete_user_ac_after_off_status function: {e}")


def user_assign_duration_calculation():
    try:
        user_rooms = UserRoomAssign.objects.all()
        for user_room in user_rooms:
            user = user_room.user

            user_acs = UserACAssign.objects.filter(user=user, room=user_room.room, ac__ac_esp=True)

            room_duration_over = RoomDurationOver.objects.filter(user=user, room=user_room.room,
                                                              duration=user_room.duration, is_time_over=False).exists()
            if room_duration_over and user_acs:
                room_duration_over = RoomDurationOver.objects.get(user=user, room=user_room.room,
                                                                     duration=user_room.duration,
                                                                     is_time_over=False)
                remain_duration = room_duration_over.remain_duration
                if remain_duration <= datetime.timedelta(hours=0, minutes=0, seconds=0):
                    room_duration_over.is_time_over = True
                    room_duration_over.save()
                    user_room.duration = datetime.timedelta(hours=0, minutes=0, seconds=0)
                    user_room.save()
                else:
                    ac_duration = remain_duration / user_acs.count()
                    for user_ac in user_acs:
                        current_time = timezone.localtime()
                        user_ac.endTime = current_time
                        user_ac.save()
                        if not current_time - user_ac.get_startTime() <= ac_duration:
                            user_ac.ac.ac_esp = False
                            user_ac.endTime = current_time
                            room_duration_over.remain_duration = room_duration_over.remain_duration - (user_ac.endTime - user_ac.startTime)
                            room_duration_over.save()
                            user_ac.ac.save()
                            user_ac.delete()

                            if room_duration_over.remain_duration <= datetime.timedelta(hours=0, minutes=0, seconds=0):
                                room_duration_over.is_time_over = True
                                room_duration_over.save()
                                user_room.duration = datetime.timedelta(hours=0, minutes=0, seconds=0)
                                user_room.save()

                            change_log_status_after_time_over(user_ac.ac)
    except Exception as e:
        print(f"Exception occur in user_assign_duration_calculation function: {e}")


def change_log_status_after_time_over(ac):
    try:
        log = Logs.objects.filter(ac_name=ac.name, on_by__isnull=False, status='ON', on_time__isnull=False,
                                   off_by__isnull=True,  off_time__isnull=True).exists()
        if log:
            log = Logs.objects.get(ac_name=ac.name, on_by__isnull=False, status='ON', on_time__isnull=False,
                                      off_by__isnull=True, off_time__isnull=True)

            log.off_by = 'Allocated Time is Over'
            log.status = 'OFF'
            off_time = ac.get_updated_at_time()
            log.off_time = off_time
            total_on_time = off_time - log.get_ist_on_time()
            log.total_on_time = total_on_time

            total_ac_working_hours = ac.total_ac_working_hours

            if total_ac_working_hours:
                total_ac_working_hours = total_ac_working_hours + total_on_time
                log.total_ac_working_hours = total_ac_working_hours
            else:
                total_ac_working_hours = total_on_time
                log.total_ac_working_hours = total_ac_working_hours

            ac.total_ac_working_hours = total_ac_working_hours
            ac.save()
            log.save()

    except Exception as e:
        print(f"Exception occur in change_log_status_after_time_over function: {e}")


def loop_thread():
    try:
        while True:
            user_assign_duration_calculation()
            time.sleep(1)
    except Exception as e:
        print(f"Exception occur in loop_thread function: {e}")