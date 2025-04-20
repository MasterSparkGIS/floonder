import copy
from datetime import datetime

from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from users.models import User
from users.serializers.serializers_roles import RoleSerializer


class UserSerializer(serializers.ModelSerializer):
    role = RoleSerializer(read_only=True)

    class Meta:
        model = User
        fields = [
            'name',
            'email',
            'password',
            'role',
            'phone_number',
            'profile_uri',
            'created_at',
            'updated_at',
            'created_by',
            'updated_by',
            'active',
        ]

        extra_kwargs = {
            'password': {
                'write_only': True
            },
        }

        required_fields = [
            'nim',
            'name',
            'email',
            'password',
            'role',
            'phone_number',
            'profile_uri',
        ]

        read_only_fields = [
            'created_at',
            'updated_at',
            'created_by',
            'updated_by',
        ]

    def get_fields(self):
        fields = super(UserSerializer, self).get_fields()

        request = self.context.get('request', None)
        if request and getattr(request, 'method', None) == "PATCH":
            for field in self.Meta.required_fields:
                fields[field].required = False

        return fields

    def to_internal_value(self, data):
        new_data = copy.deepcopy(data)

        return super().to_internal_value(new_data)

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))

        if self.context['request'].user.is_authenticated:
            validated_data['created_by'] = self.context['request'].user.email
            validated_data['updated_by'] = self.context['request'].user.email
        else:
            validated_data['created_by'] = "system"
            validated_data['updated_by'] = "system"

        return super(UserSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        validated_data['updated_at'] = datetime.now()
        validated_data['updated_by'] = self.context['request'].user.email

        return super(UserSerializer, self).update(instance, validated_data)

    def delete(self, instance):
        instance.active = False
        instance.save()

        return instance

    def get_role(self, obj):
        return obj.role


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'role', 'phone_number', 'profile_uri']

    def to_representation(self, instance):
        response = super().to_representation(instance)

        return response
