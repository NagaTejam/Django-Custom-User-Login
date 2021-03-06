from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import datetime

class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    sys_id = models.AutoField(primary_key=True, blank=True)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    first_name = models.CharField(max_length=50,blank=True,null=True)
    last_name = models.CharField(max_length=50,blank=True,null=True)
    address = models.TextField(max_length=300,blank=True,null=True)
    DOB = models.DateField('Date of Birth', blank=True, null=True)
    DOJ = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False) # a admin user; non super-user
    admin = models.BooleanField(default=False) # a superuser
    # notice the absence of a "Password field", that's built in.
    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['first_name','last_name'] # Email & Password are required by default.

    def get_full_name(self):
        # The user is identified by their email address
        return self.last_name+first_name

    def get_short_name(self):
        # The user is identified by their email address
        return self.first_name

    def __str__(self):              # __unicode__ on Python 2
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

    @property
    def is_active(self):
        "Is the user active?"
        return self.active

class services(models.Model):
    taskid = models.AutoField(primary_key=True, blank=True)
    client = models.CharField(max_length=50,blank=True,null=True)
    project = models.CharField(max_length=50,blank=True,null=True)
    taskTime = models.DateTimeField('Task Time', blank=True, null=True)
    hours = models.TimeField(blank=True, null=True)
    minutes = models.TimeField(blank=True, null=True)
    Description = models.TextField(max_length=300,blank=True,null=True)
    email = models.OneToOneField(User, on_delete=models.CASCADE)
