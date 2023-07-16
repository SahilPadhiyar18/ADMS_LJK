from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser
import uuid
from django.contrib.auth.hashers import make_password

# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, password2=None):
        """
        Creates and saves a User with the given email, name, and password.
        """
        if not email:
            raise ValueError('User must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            username=username           
        )
        user.set_password(password)
        user.save(using=self._db)
        
        return user

    def create_superuser(self, username, email, password=None):
        """
        Creates and saves a superuser with the given email, name, and password.
        """
        user = self.create_user(
            username=username,
            email=email,
            password=password,
        )
        user.user_type = 1
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


#  Custom User Model
class User(AbstractBaseUser):
    USER_TYPE_CHOICES = (
      (1, 'admin'),
      (2, 'technician'),
      (3, 'regular')
    )

    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, blank=True, null=True)
    username = models.CharField(max_length=200, unique=True)
    email = models.EmailField(
        verbose_name='Email',
        max_length=255,
        unique=True,
    )
    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, default=3)
    is_admin = models.BooleanField(default=False)
    phone = models.CharField(max_length=12, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __unicode__(self):
        return self.user_id

    def __str__(self):
        return self.username
    
    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    def save(self, *args, **kwargs):
        if not self.password.startswith('pbkdf2_'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)