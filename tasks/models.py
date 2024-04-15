from django.db import models
from django.contrib.auth.models import User


# Create your models here.


# * Tasks models

class Tasks(models.Model):
    title = models.CharField(max_length=150)
    description = models.CharField(max_length=350)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    important = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title + ' - ' + self.user.username
