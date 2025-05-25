import uuid
from django.test import TestCase, override_settings
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile

from .models_roles import Role

User = get_user_model()


@override_settings(MEDIA_ROOT="/tmp/django_test_media/")
class UserModelTests(TestCase):
    def setUp(self):
        self.role_super  = Role.objects.create(id=uuid.uuid4(), name="Super User")
        self.role_admin  = Role.objects.create(id=uuid.uuid4(), name="Admin")
        self.role_member = Role.objects.create(id=uuid.uuid4(), name="User")

        dummy_img = SimpleUploadedFile(
            name="avatar.jpg",
            content=b"filecontent",
            content_type="image/jpeg"
        )

        self.u_super = User.objects.create(
            id=uuid.uuid4(),
            role=self.role_super,
            name="Root",
            email="root@example.com",
            phone_number="111",
            profile_uri=dummy_img,
            active=True,
            created_by="test",
            updated_by="test",
        )

        self.u_admin = User.objects.create(
            id=uuid.uuid4(),
            role=self.role_admin,
            name="Alice",
            email="admin@example.com",
            phone_number="222",
            profile_uri=dummy_img,
            active=True,
            created_by="test",
            updated_by="test",
        )

        self.u_member = User.objects.create(
            id=uuid.uuid4(),
            role=self.role_member,
            name="Bob",
            email="user@example.com",
            phone_number="333",
            profile_uri=dummy_img,
            active=True,
            created_by="test",
            updated_by="test",
        )

    def test_is_superuser(self):
        self.assertTrue(self.u_super.is_superuser())
        self.assertFalse(self.u_admin.is_superuser())
        self.assertFalse(self.u_member.is_superuser())

    def test_is_admin(self):
        self.assertTrue(self.u_admin.is_admin())
        self.assertFalse(self.u_super.is_admin())
        self.assertFalse(self.u_member.is_admin())

    def test_is_user(self):
        self.assertTrue(self.u_member.is_user())
        self.assertFalse(self.u_super.is_user())
        self.assertFalse(self.u_admin.is_user())

    def test_is_active_tercermin_dari_field_active(self):
        # default aktif
        self.assertTrue(self.u_member.is_active())

        # ubah jadi non-aktif
        self.u_member.active = False
        self.u_member.save(update_fields=["active"])
        self.assertFalse(self.u_member.is_active())

    def test_dunder_str_mengembalikan_email(self):
        self.assertEqual(str(self.u_admin), "admin@example.com")
        self.assertEqual(str(self.u_member), "user@example.com")