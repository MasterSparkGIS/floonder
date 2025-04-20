import uuid

from django.contrib.auth.base_user import BaseUserManager

from .models import Role


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        uid = uuid.uuid4()
        user = self.model(id=uid, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        role = Role.objects.get(name='Super User')
        extra_fields.setdefault('role_id', role.id)
        return self.create_user(email, password, **extra_fields)
