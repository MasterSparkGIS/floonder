from django.db import models


class Role(models.Model):
    id = models.UUIDField(primary_key=True, editable=False)
    name = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now_add=True, null=True)

    created_by = models.CharField(null=True, max_length=255, default="system")
    updated_by = models.CharField(null=True, max_length=255, default="system")

    def __str__(self):
        return self.name
