from django.db import models
from  django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

# Create your models here.

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)



class CustomUserModel(AbstractBaseUser, PermissionsMixin):
    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        app_label = 'apps_users'
        db_table = 'users'


    # defauld fields
    email = models.EmailField(unique=True)
    username = models.TextField(max_length=15, unique=True, blank=True, null=True)

    
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)

    # custom fields
    full_name = models.TextField(max_length=100, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='users/profile_pictures/', blank=True, null=True)
    pronouns = models.TextField(max_length=20, blank=True, null=True)
    age_group = models.TextField(max_length=20, blank=True, null=True)
    life_situation = models.TextField(max_length=100, blank=True, null=True)
    occupation = models.TextField(max_length=50, blank=True, null=True)
    life_feelings = models.TextField(blank=True, null=True)
    faith = models.TextField(max_length=50, blank=True, null=True)
    inspiration_sources = models.TextField(blank=True, null=True)
    attention_today = models.TextField(blank=True, null=True)


    # Verification Trackers
    is_email_verified = models.BooleanField(default=False)

    # We will reuse this field for OTPs, or create two separate ones
    verification_code = models.CharField(max_length=6, blank=True, null=True)

    # The account is only usable if BOTH are True
    is_active = models.BooleanField(default=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    