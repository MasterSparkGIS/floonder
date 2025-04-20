from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models

from .managers import UserManager
from .models_roles import Role


class User(AbstractBaseUser):
    id = models.UUIDField(primary_key=True, editable=False)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(unique=True, max_length=255)
    profile_uri = models.ImageField(upload_to="uploads/user/profile/")

    active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now_add=True, null=True)

    created_by = models.CharField(null=True, max_length=255)
    updated_by = models.CharField(null=True, max_length=255)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number']

    objects = UserManager()

    def is_superuser(self):
        return self.role.name == "Superuser"

    def is_admin(self):
        return self.role.name == "Admin"

    def is_user(self):
        return not self.is_superuser() and not self.is_admin()

    def is_active(self):
        return self.active

    def __str__(self):
        return self.email
