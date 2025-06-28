from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
import random
from django.core.validators import RegexValidator
from django.forms import ValidationError


#validator
business_username_validator = RegexValidator(
                                regex=r'^[a-zA-Z_]+$', 
                                message='Username can only contain letters and underscores.', 
                                code='invalid_username')

# Create your models here.

class CustomUserManager(BaseUserManager):

    def create_user(self, email, first_name, last_name, password, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        if not password:
            raise ValueError("Password is required")
        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        if not password:
            raise ValueError("Password is required")
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, first_name, last_name, password, **extra_fields)


class CustomAccounts(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=7, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_brandowner = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    def save(self, *args, **kwargs):
        if not self.pk and not self.username:
            base = self.first_name[:4].upper() if len(self.first_name) >= 4 else self.first_name.upper()
            while True:
                candidate = base + str(random.randint(100, 999))
                if not CustomAccounts.objects.filter(username=candidate).exists():
                    self.username = candidate
                    break
        super().save(*args, **kwargs)


    def update_password(self, new_password):
        self.set_password(new_password)
        self.save(update_fields=["password"])

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.first_name + " " + self.last_name

    def get_short_name(self):
        return self.first_name


class UserProfile(models.Model):
    user = models.OneToOneField(CustomAccounts, on_delete=models.CASCADE, related_name="profile")
    phone_number = models.CharField(max_length=100)
    dob = models.DateField(auto_now=False, auto_now_add=False)
    address = models.CharField(max_length=100)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=10)

    

class BrandProfile(models.Model):
    username = models.CharField(max_length=50, unique=True, validators=[business_username_validator])
    owner = models.OneToOneField(CustomAccounts, on_delete=models.CASCADE, related_name="brand")
    brand_name = models.CharField(max_length=50)
    brand_logo = models.ImageField(upload_to="brand_logos/", max_length=None, default="/media/brand.png")
    brand_media = models.URLField(max_length=200)
    business_number = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    

    def clean(self):
        if not self.owner.is_brandowner:
            raise ValidationError("Only users marked as brand owners can be assigned a brand profile.")

    def __str__(self):
        return self.username
    



