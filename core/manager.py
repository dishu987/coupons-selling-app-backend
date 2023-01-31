from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser



#  Custom User Manager
class UserManager(BaseUserManager):
  def create_user(self, email, password=None, password2=None,**extra_fields):
      """
      Creates and saves a User with the given email, name, tc and password.
      """
      if not email:
          raise ValueError('User must have an email address')

      user = self.model(
          email=self.normalize_email(email),
          **extra_fields
      )

      user.set_password(password)
      user.save(using=self._db)
      return user

  def create_superuser(self, email, name, password=None):
    """
    Creates and saves a superuser with the given email, name, tc and password.
    """
    user = self.create_user(
        email=self.normalize_email(email),
        name=name
    )
    user.set_password(password)
    user.staff = True
    user.active = True
    user.is_admin = True
    user.save(using=self._db)
    return user
