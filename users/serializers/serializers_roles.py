import uuid
from datetime import datetime

from rest_framework import serializers

from users.models import Role


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'

        required_fields = [
            'name',
        ]

        read_only_fields = [
            'id',
            'created_at',
            'updated_at',
            'created_by',
            'updated_by'
        ]

    def create(self, validated_data):

        if self.context['request'].user.is_authenticated:
            validated_data['created_by'] = self.context['request'].user.nim
            validated_data['updated_by'] = self.context['request'].user.nim
        else:
            validated_data['created_by'] = "system"
            validated_data['updated_by'] = "system"

        validated_data['id'] = uuid.uuid4()

        return super(RoleSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        validated_data['updated_at'] = datetime.now()
        validated_data['updated_by'] = self.context['request'].user.nim

        return super(RoleSerializer, self).update(instance, validated_data)

    def to_representation(self, instance):
        response = super().to_representation(instance)

        response['id'] = response.pop('id', None)
        response['name'] = response.pop('name', None)
        response['createdAt'] = response.pop('created_at', None)
        response['updatedAt'] = response.pop('updated_at', None)
        response['createdBy'] = response.pop('created_by', None)
        response['updatedBy'] = response.pop('updated_by', None)

        return response
