from django import forms
from .models import *


class UploadExcelForm(forms.Form):
    excel_file = forms.FileField()


class CircuitForm(forms.ModelForm):
    def clean(self):
        try:
            esp_id = self.cleaned_data['esp_id']
        except Exception as e:
            esp_id = None
        if esp_id:
            esp_id = esp_id.upper()

            if self.instance and self.instance.esp_id == esp_id:
                return  # Skip validation if updating the same object

            if esp_id and Circuit.objects.filter(esp_id=esp_id).exists():
                raise forms.ValidationError({'esp_id': f"{esp_id} already exists"})


class RoomForm(forms.ModelForm):
    def clean(self):
        try:
            room_id = self.cleaned_data['room_id']
        except Exception as e:
            room_id = None
        if room_id:
            room_id = room_id.upper()

            if self.instance and self.instance.room_id == room_id:
                return  # Skip validation if updating the same object

            if room_id and Room.objects.filter(room_id=room_id).exists():
                raise forms.ValidationError({'room_id': f"{room_id} already exists"})


class ACForm(forms.ModelForm):
    def clean(self):
        try:
            cleaned_data = super().clean()
            name = self.cleaned_data['name']
        except Exception as e:
            name = None
        if name:
            name = name.upper()
            circuit = self.cleaned_data['circuit']
            room = self.cleaned_data['room']
            if self.instance and self.instance.name == name:
                return  # Skip validation if updating the same object

            if name and AC.objects.filter(room=room, circuit=circuit, name=name).exists():
                raise forms.ValidationError({'name': f"{name} already exists"})
            if AC.objects.filter(circuit=circuit).count() >= 3:
                raise forms.ValidationError({'circuit': f"3 ACs already exists for this circuit can not add more than 3 ACs in One Circuit"})
