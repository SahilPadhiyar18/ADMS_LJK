from adms_logs.models import Logs
from django.db.models import Sum
from .models import UserRoomAssign, AC
from accounts.models import User
from django.utils import timezone


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
            total_ac_working_hours = Logs.objects.filter(ac_name=ac.name).aggregate(total_hours=Sum('total_on_time'))['total_hours']
            
            if log_exist:
                if total_ac_working_hours:
                    log.total_ac_working_hours = total_ac_working_hours + total_on_time
                else:
                    log.total_ac_working_hours = total_on_time   
            else:
                log.total_ac_working_hours = total_ac_working_hours
        elif field == 'ac_lock' and task_perform:
            log.task = 'LOCK'    
        
        if task_perform:
            log.save()

        print('log successfully added/updated')
    except Exception as e:
        print(f'getting log related errror {e} can not add/update log for {ac.name}')    



def check_user_assign_time_for_ac():
    logs = Logs.objects.filter(task='ON/OFF').filter(on_time__isnull=False).filter(on_by__isnull=False). \
            filter(off_time__isnull=True).filter(off_by__isnull=True)
            
    for log in logs:
        user_name = log.on_by
        user_room = UserRoomAssign.objects.get(user__username=user_name)
        user_room_assign_time = user_room.get_updated_at_time() + user_room.duration
        current_time = timezone.localtime()       
        if current_time > user_room_assign_time:
            log.off_time = current_time
            log.off_by = 'Allocated Time is Over'
            
            ac = AC.objects.get(name=log.ac_name)
            ac.ac_esp = False
            ac.save()

            total_on_time = current_time - log.on_time
            log.total_on_time = total_on_time
            
            total_ac_working_hours = Logs.objects.filter(ac_name=ac.name).aggregate(total_hours=Sum('total_on_time'))['total_hours']
            
            if total_ac_working_hours:
                log.total_ac_working_hours = total_ac_working_hours + total_on_time
            else:
                log.total_ac_working_hours = total_on_time   
            
            log.save()
            print('log check success')

