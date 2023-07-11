import datetime

from django.db import models
import uuid
from accounts.models import User
from django.utils import timezone

# Create your models here.

    
class Room(models.Model):
    user = models.ManyToManyField(User, blank=True)
    room_uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) 
    room_id = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return self.room_id
    
    def save(self, *args, **kwargs):
        timezone.activate('Asia/Kolkata')
        self.created_at = timezone.localtime(self.created_at)
        self.updated_at = timezone.localtime(self.updated_at)

        self.room_id = self.room_id.upper()
        is_new_obj = Room.objects.filter(pk=self.pk).exists()
        if not is_new_obj:
            if self.room_id and Room.objects.filter(room_id=self.room_id).exists():
                return
            super().save(*args, **kwargs)
        else:
            super().save(*args, **kwargs)    

    def clean(self):
        if self.pk and self.user.exists():
            return        


class Circuit(models.Model):
    ckt_uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) 
    panel_id = models.CharField(max_length=255)
    esp_id = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return f"Ckt - > {self.esp_id}"

    def save(self, *args, **kwargs):
        timezone.activate('Asia/Kolkata')
        self.created_at = timezone.localtime(self.created_at)
        self.updated_at = timezone.localtime(self.updated_at)

        self.esp_id = self.esp_id.upper()
        is_new_obj = Circuit.objects.filter(pk=self.pk).exists()
        if not is_new_obj:
            if self.esp_id and Circuit.objects.filter(esp_id=self.esp_id).exists():
                return
            super().save(*args, **kwargs)
        else:
            super().save(*args, **kwargs)    
    

class AC(models.Model):
    ac_uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) 
    room = models.ForeignKey(Room, on_delete=models.CASCADE, null=True, blank=True)
    circuit = models.ForeignKey(Circuit, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255)
    ac_esp = models.BooleanField(default=False)
    lock = models.BooleanField(default=False)
    ping = models.DateTimeField(blank=True, null=True)
    status = models.BooleanField(default=False)
    no = models.IntegerField(blank=True, null=True)
    total_ac_working_hours = models.DurationField(null=True, blank=True, default=datetime.timedelta(hours=0, minutes=0, seconds=0))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return f"{self.name} - {self.room.room_id} - {self.circuit.esp_id}"
    
    def get_created_at_time(self):
        return timezone.localtime(self.created_at)
    
    def get_updated_at_time(self):
        return timezone.localtime(self.updated_at)
 
    def save(self, *args, **kwargs):
        timezone.activate('Asia/Kolkata')
        self.created_at = timezone.localtime(self.created_at)
        self.updated_at = timezone.localtime(timezone.now())

        is_new_obj = AC.objects.filter(pk=self.pk).exists()

        self.name = self.name.upper()
        if not is_new_obj:
            self.no = AC.objects.filter(circuit=self.circuit).count() + 1
            if AC.objects.filter(room=self.room, circuit=self.circuit, name=self.name).exists():
                return
            if AC.objects.filter(circuit=self.circuit).count() >= 3:
                return
            super().save(*args, **kwargs)
        else:
            super().save(*args, **kwargs)
        
        

        
      

            