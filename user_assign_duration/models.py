from main_app.models import *

# Create your models here.


class UserRoomAssign(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, null=True, blank=True)
    duration = models.DurationField(blank=True, null=True)
    remain_duration = models.DurationField(blank=True, null=True)
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
        self.remain_duration = self.duration

        if not self.user:
            return
        elif self.room is None:
            return
        elif self.duration is None:
            return

        elif self.room and self.duration and self.user:
            if self.user.is_admin:
                return

            if UserRoomAssign.objects.filter(room=self.room, user=self.user).exists():
                user_room = UserRoomAssign.objects.get(room=self.room, user=self.user)
                if user_room.duration != self.duration:
                    user_room.delete()

            if not self.user.is_admin:
                room_duration_over = RoomDurationOver.objects.filter(user=self.user, room=self.room).exists()
                if room_duration_over:
                    room_dur_obj = RoomDurationOver.objects.get(user=self.user, room=self.room)
                    room_dur_obj.delete()

                new_room_duration_over = RoomDurationOver(user=self.user, room=self.room, duration=self.duration, remain_duration=self.duration, is_time_over=False)
                new_room_duration_over.save()

            self.room.user.add(self.user)

        super().save(*args, **kwargs)

    def delete(self, using=None, keep_parents=False):
        try:
            self.room.user.remove(self.user)
            super().delete(using=using, keep_parents=keep_parents)

            if RoomDurationOver.objects.filter(user=self.user, room=self.room, duration=self.duration).exists():
                RoomDurationOver.objects.get(user=self.user, room=self.room, duration=self.duration).delete()

        except Exception as e:
            print(f'Exception occur in delete method of UserRoomAssign model. {e}')


class UserACAssign(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, null=True, blank=True)
    ac = models.ForeignKey(AC, on_delete=models.CASCADE, null=True, blank=True)
    duration = models.DurationField(blank=True, null=True)
    startTime = models.DateTimeField()
    endTime = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.ac} - ({self.duration})"

    def get_created_at_time(self):
        return timezone.localtime(self.created_at)

    def get_updated_at_time(self):
        return timezone.localtime(self.updated_at)

    def get_startTime(self):
        return timezone.localtime(self.startTime)

    def get_endTime(self):
        return timezone.localtime(self.endTime)

    def save(self, *args, **kwargs):
        timezone.activate('Asia/Kolkata')
        self.created_at = timezone.localtime(self.created_at)
        self.updated_at = timezone.localtime(timezone.now())
        super().save(*args, **kwargs)


class RoomDurationOver(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, null=True, blank=True)
    duration = models.DurationField(blank=True, null=True)
    remain_duration = models.DurationField(blank=True, null=True)
    is_time_over = models.BooleanField(blank=True, null=True, default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user} - {self.room} - ({self.duration})- (Remain Time: {self.remain_duration})"

    def save(self, *args, **kwargs):
        timezone.activate('Asia/Kolkata')
        self.created_at = timezone.localtime(self.created_at)
        self.updated_at = timezone.localtime(timezone.now())
        super().save(*args, **kwargs)