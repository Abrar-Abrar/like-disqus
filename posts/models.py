from django.db import models
from django.conf import settings
from django import forms
from django.contrib.auth import get_user_model
# Create your models here.

User = get_user_model()


class Post(models.Model):
    author = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, null=True, blank=True)
    content = models.CharField(max_length=1000)
    image = models.ImageField(upload_to='posts/', null=True, blank=True)
    likes = models.ManyToManyField(
        User, blank=True, related_name='post_likes')
    dislikes = models.ManyToManyField(
        User, blank=True, related_name='post_dislikes')
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return str(self.author) + "'s post"
