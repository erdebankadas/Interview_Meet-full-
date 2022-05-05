from django.db import models
from django.conf import settings

# Create your models here.
class Resume(models.Model):
    data = models.TextField(null=True)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.RESTRICT,
    )

    def __str__(self):
        return self.user.username