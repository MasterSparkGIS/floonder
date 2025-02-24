# Generated by Django 5.0.3 on 2025-02-18 20:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.UUIDField(editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('created_by', models.CharField(default='system', max_length=255, null=True)),
                ('updated_by', models.CharField(default='system', max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('id', models.UUIDField(editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('phone_number', models.CharField(max_length=255, unique=True)),
                ('profile_uri', models.ImageField(upload_to='uploads/user/profile/')),
                ('active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('created_by', models.CharField(max_length=255, null=True)),
                ('updated_by', models.CharField(max_length=255, null=True)),
                (
                'role_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.role')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
