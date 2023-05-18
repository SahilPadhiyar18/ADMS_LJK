from django.db import models
import uuid
from accounts.models import User
from django.utils import timezone

from django.db.models.signals import m2m_changed
from django.dispatch import receiver
# Create your models here.

    
class Room(models.Model):
    user = models.ManyToManyField(User, blank=True, editable=False)
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
    name = models.CharField(max_length=255, unique=True)
    ac_esp = models.BooleanField(default=False)
    lock = models.BooleanField(default=False)
    ping = models.DateTimeField()
    status = models.BooleanField(default=False)
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
            if self.name and AC.objects.filter(name=self.name).exists():
                return
            if AC.objects.filter(circuit=self.circuit).count() >= 3:
                return
            super().save(*args, **kwargs)
        else:
            super().save(*args, **kwargs)
        
        
class UserRoomAssign(models.Model):
    user = models.ManyToManyField(User, blank=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, null=True, blank=True)
    duration = models.DurationField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return f"{self.room} - ({self.duration})"
    
    def get_created_at_time(self):
        return timezone.localtime(self.created_at)
    
    def get_updated_at_time(self):
        return timezone.localtime(self.updated_at)
 
    def save(self, *args, **kwargs):
        timezone.activate('Asia/Kolkata')
        self.created_at = timezone.localtime(self.created_at)
        self.updated_at = timezone.localtime(timezone.now())
        super().save(*args, **kwargs)
        
      
@receiver(m2m_changed, sender=UserRoomAssign.user.through)
def userroomassign_users_changed(sender, instance, action, **kwargs):
    room = instance.room
   
    if action == 'post_add' or action == 'post_clear':
        users = instance.user.all()
        room.user.set(users)    
            