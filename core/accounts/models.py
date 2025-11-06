from django.db import models
from django.contrib.auth.models import (AbstractBaseUser , BaseUserManager , PermissionsMixin) 
from django.utils.translation import gettext_lazy as _ 



class UserManager(BaseUserManager):
    """
    Custom User Manager where email is the unique identifiers instead of username 
    """
    def create_user(self,email,password=None,**extra_fields):
        if not email:
            raise ValueError(_("The Email must be set"))
        user = self.model(email=self.normalize_email(email),**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self,email,password=None,**extra_fields):
        extra_fields.setdefault("is_staff",True)
        extra_fields.setdefault("is_superuser",True)
        extra_fields.setdefault("is_active",True)
        extra_fields.setdefault("is_verified",True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True"))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True"))
        
        user = self.create_user(email,password,**extra_fields)
        return user



# Create your models here.

class User(AbstractBaseUser,PermissionsMixin):
    """
    Custom User Model for our app 
    """
    email = models.EmailField(max_length=250,unique=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)

    USERNAME_FIELD = "email"  
    REQUIRED_FIELDS = []  

    created_joined = models.DateTimeField(auto_now_add=True) 
    updated = models.DateTimeField(auto_now=True)

    objects = UserManager()

    def __str__(self):
        return self.email
    

        

class Profile(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    image = models.ImageField(null=True,blank=True)
    description = models.TextField()
    created_joined = models.DateTimeField(auto_now_add=True) 
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.email
    

