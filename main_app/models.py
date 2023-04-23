from django.db import models
import uuid
from accounts.models import User

# Create your models here.


class Room(models.Model):
    room_uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) 
    room_id = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return self.room_id
    
class Circuit(models.Model):
    ckt_uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) 
    panel_id = models.CharField(max_length=255)
    esp_id = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return f"Ckt - > {self.panel_id}"
    
class AC(models.Model):
    user = models.ManyToManyField(User, blank=True)
    ac_uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) 
    room = models.ForeignKey(Room, on_delete=models.CASCADE, null=True, blank=True)
    circuit = models.ForeignKey(Circuit, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255)
    ac_esp = models.BooleanField(default=False)
    lock = models.BooleanField(default=False)
    ping = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 

   
    def __str__(self):
        return f"{self.name} - {self.room.room_id} - {self.circuit.panel_id}"
    
 
    def save(self, *args, **kwargs):
        is_new_obj = AC.objects.filter(pk=self.pk).exists()
        
        if not is_new_obj:
            if self.name and AC.objects.filter(name=self.name).exists():
                # raise ValueError("This AC is already assigned to a different room.")
                return
            if AC.objects.filter(circuit=self.circuit).count() >= 2:
                # raise ValueError("Can not add more than 2 AC in one Circuit ")
                return
            super().save(*args, **kwargs)
        else:
            super().save(*args, **kwargs)
        
        



    
