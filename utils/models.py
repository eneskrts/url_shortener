from django.contrib.auth import get_user_model
from django.db import models


user_model = get_user_model()

class UrlBaseModel(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        user_model,
        on_delete=models.CASCADE,
        related_name='%(class)s_created_by',
        null=True,
        blank=True
    )
    updated_by = models.ForeignKey(
        user_model,
        on_delete=models.CASCADE,
        related_name='%(class)s_updated_by',
        null=True,
        blank=True
    )
    class Meta:
        abstract = True


    def save(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        if user:
            if not self.pk:
                self.created_by = self.created_by or user
            self.updated_by = user
        super().save(*args, **kwargs)