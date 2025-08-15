from django.db import models
from django.contrib.auth.models import AbstractBaseUser

from accounts.managers import UserManager
from utils.models import BaseABCModel


# Create your models here.
class User(BaseABCModel, AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    private_id = models.CharField(max_length=255, editable=False)
    username = models.CharField(max_length=255, unique=True)
    last_name = models.CharField(max_length=255)
    verified_at = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True, blank=True)
    is_superuser = models.BooleanField(default=False, blank=True)
    is_staff = models.BooleanField(default=False, blank=True)

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "username"]

    objects = UserManager()

    class Meta(BaseABCModel.Meta):
        indexes = [
            models.Index(fields=["id"]),
            models.Index(fields=["email"]),
            models.Index(fields=["-created_at"]),
        ]

    def __str__(self) -> str:
        return self.email

    def save(self, *args, **kwargs) -> None:
        self.email = self.email.lower()
        super(User, self).save(*args, **kwargs)

    def has_perm(self, perm, obj=None) -> bool:
        """django internal use"""
        return self.is_superuser

    def has_module_perms(self, app_label) -> bool:
        """django internal use"""
        return self.is_superuser


    @property
    def name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    @property
    def initial(self) -> str:
        return f"{self.first_name[0]}{self.last_name[0]}".upper()

    @property
    def is_verified(self) -> bool:
        return bool(self.verified_at)




