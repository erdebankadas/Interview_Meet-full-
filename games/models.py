from django.db import models
from django.conf import settings

# Create your models here.
class Game(models.Model):
    name = models.CharField(max_length=50)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.RESTRICT,
    )
    data = models.TextField()
    score = models.TextField()
    started_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)