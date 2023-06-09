from django.contrib import admin
from .models import User

# Register your models here.


class UserAdmin(admin.ModelAdmin):
    change_list_template = 'admin/User_change_list.html'
    list_display = ('username', 'email', 'user_type')
    search_fields = ['username', 'email']


admin.site.register(User, UserAdmin)
