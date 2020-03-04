from django.db import models

from django.contrib.auth.models import User


class Todo(models.Model):
    title = models.CharField(max_length=100)
    # TextField(blank=True) means that user does not have to fill out this field
    memo = models.TextField(blank=True)
    created_time = models.DateTimeField(auto_now_add=True)
    completed_time = models.DateTimeField(null=True, blank=True)
    important = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} - {self.user}"
