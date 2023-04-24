from django.db import models
import uuid
from accounts.models import User

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
        self.room_id = self.room_id.upper()
        is_new_obj = Room.objects.filter(pk=self.pk).exists()
        if not is_new_obj:
            if self.room_id and Room.objects.filter(room_id=self.room_id).exists():
                return
            super().save(*args, **kwargs)
        else:
            super().save(*args, **kwargs)    
    
class Circuit(models.Model):
    ckt_uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) 
    panel_id = models.CharField(max_length=255)
    esp_id = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return f"Ckt - > {self.esp_id}"

    def save(self, *args, **kwargs):
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
    
 
    def save(self, *args, **kwargs):
        is_new_obj = AC.objects.filter(pk=self.pk).exists()
        
        self.name = self.name.upper()
        if not is_new_obj:
            if self.name and AC.objects.filter(name=self.name).exists():
                return
            if AC.objects.filter(circuit=self.circuit).count() >= 2:
                return
            super().save(*args, **kwargs)
        else:
            super().save(*args, **kwargs)
        
        



    
