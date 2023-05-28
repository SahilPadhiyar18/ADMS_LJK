from django.shortcuts import render
from .models import Logs
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
# from main_app.utils import check_user_assign_time_for_ac
from django.shortcuts import redirect
# Create your views here.

@login_required(login_url='login')
def logs_view(request):
    if request.user.is_admin:
        # check_user_assign_time_for_ac()
        if request.method == 'POST' and request.POST['ac_name']: 
            ac_name = request.POST['ac_name']
            logs = Logs.objects.filter(ac_name=ac_name.upper()).order_by('-id')
            template_name = 'main_templates/search_logs.html'
        else:    
            logs = Logs.objects.all().order_by('-id')
            template_name = 'main_templates/logs.html'

        paginator = Paginator(logs, 12) 
        
        page_number = request.GET.get("page")
        logs_page = paginator.get_page(page_number) 

        context = {
            'logs': logs_page
        }
        return render(request, template_name, context)
    else:
        return redirect('home')

