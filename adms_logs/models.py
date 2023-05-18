from django.db import models
from django.utils import timezone

# Create your models here.


class Logs(models.Model):
    ac_name = models.CharField(null=True, blank=True, max_length=100)
    task = models.CharField(null=True, blank=True, max_length=100)
    on_by = models.CharField(null=True, blank=True, max_length=100)
    off_by = models.CharField(null=True,blank=True, max_length=100)
    status = models.CharField(null=True, blank=True, max_length=100)
    on_time = models.DateTimeField(null=True)
    off_time = models.DateTimeField(null=True)
    total_on_time = models.DurationField(null=True, blank=True) # off_time - on_time
    total_ac_working_hours = models.DurationField(null=True, blank=True) # sum of total_on_time
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return self.ac_name
    
    def formatted_total_on_time(self):
        return str(self.total_on_time).split('.')[0]
    
    def formatted_total_ac_working_hours(self):
        return str(self.total_ac_working_hours).split('.')[0]
    
    def save(self, *args, **kwargs):
        timezone.activate('Asia/Kolkata')
        self.created_at = timezone.localtime(self.created_at)
        self.updated_at = timezone.localtime(self.updated_at)
        super().save(*args, **kwargs)    