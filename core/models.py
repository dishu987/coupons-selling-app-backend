from django.db import models
import datetime
from datetime import timedelta
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .manager import UserManager
from django.utils.translation import gettext as _
from django.utils import timezone
import uuid

HOSTELS = (
        ('Satluj East', 'Satluj East'),
        ('Satluj West', 'Satluj West'),
        ('Beas East', 'Beas East'),
        ('Beas West', 'Beas West'),
        ('Chenab East', 'Chenab East'),
        ('Chenab West', 'Chenab West'),
        ('Raavi East', 'Raavi East'),
        ('Raavi West', 'Raavi West')
    )
DEGREE = (
    ('BTECH', 'Becholer of Technology'),
    ('MTECH', 'Master of Technology'),
    ('PHD', 'PHD'),
    ('MSC', 'Master of Science'),
)
class UserModel(AbstractBaseUser, PermissionsMixin): 
    email = models.EmailField(
      verbose_name='Email',
      max_length=255,
      unique=True,
    )
    name = models.CharField(max_length=200)
    mobile = models.IntegerField(default=0)
    hostel = models.CharField(max_length=100,choices=HOSTELS)
    room = models.CharField(max_length=10,default='NA')
    degree = models.CharField(max_length=100,choices=DEGREE)
    batch = models.IntegerField(null=True,blank=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS=['name']
    #new 
    def __str__(self):
        return self.email

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

MESS = (
    ('Kanaka','Kanaka Mess'),
    ('Bhopal','Bhopal Mess')
)

TIMES = (
    ('Breakfast','Breakfast-Rs.30'),
    ('Lunch','Lunch-Rs.50'),
    ('Dinner','Dinner-Rs.60')
)
def present_or_future_date(value):
    if value < datetime.date.today():
        raise ValidationError("Coupon date cannot be in past.")
    elif datetime.date.today()+timedelta(hours=48)<value:
        raise ValidationError("Coupon cannot be more than 2 days from todays.")
    return value


class CouponModel(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=200)
    price = models.CharField(max_length=10)
    mess = models.CharField(max_length=20,choices=MESS)
    date = models.DateField(auto_now=False, auto_now_add=False,validators=[present_or_future_date])
    time = models.CharField(max_length=50,choices=TIMES)
    expired = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    class Meta:
       ordering = ('expired','date',)


class OTPModel(models.Model):
    mobile = models.CharField(max_length=10,default="",null=True,blank=True,unique=True)
    is_verified = models.BooleanField(default=False,null=True,blank=True)
    otp = models.CharField(null=True,blank=True,max_length=4)

    def __str__(self):
        return self.mobile


class Conversation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=128)
    chat_of = models.ForeignKey(UserModel, on_delete=models.CASCADE,related_name="chat_of")
    chat_to = models.ForeignKey(UserModel,on_delete=models.CASCADE,related_name="chat_to")
    online = models.BooleanField(default=False, blank=True)
    def join(self):
        self.online = True
        self.save()

    def leave(self, user):
        self.online = False
        self.save()

    def __str__(self):
        return f"{self.chat_of} ({self.chat_to})"


class Message(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation = models.ForeignKey(
        Conversation, on_delete=models.CASCADE, related_name="messages"
    )
    from_user = models.ForeignKey(
        UserModel, on_delete=models.CASCADE, related_name="messages_from_me"
    )
    to_user = models.ForeignKey(
        UserModel, on_delete=models.CASCADE, related_name="messages_to_me"
    )
    content = models.CharField(max_length=512)
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f"From {self.from_user} to {self.to_user}:[{self.timestamp}]"
