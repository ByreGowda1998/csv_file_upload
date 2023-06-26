from django.db import models
from django.contrib.auth.models import BaseUserManager ,AbstractBaseUser , PermissionsMixin
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your  custom user model here.
class UserManager(BaseUserManager):
    def create_user(self, username, email, password):
        """
        Creates and saves a User with the given email and password.
        """

        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, username, email, password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(username=username, email=email, password=password)
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(username=username, email=email, password=password)
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user



class User(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True)
    username = models.CharField(verbose_name='Username', max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False) # a admin user; non super-user
    admin = models.BooleanField(default=False) # a superuser

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username'] # Email & Password are required by default.
    objects = UserManager()
    
    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.staff

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin


from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()

class TimeStampModel(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_by_%(class)s',  blank=True, null=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='updated_by_%(class)s', blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        abstract = True
        ordering = ['-created_at', '-updated_at']

    
    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at=timezone.now()
        else:
            self.updated_at=timezone.now()
        super(TimeStampModel, self).save(*args, **kwargs)