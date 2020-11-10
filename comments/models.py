from django.db import models
from posts.models import Post
from django.contrib.auth import get_user_model
# Create your models here.

User = get_user_model()


class Comment(models.Model):
    author = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name="comments",
                             null=True, on_delete=models.CASCADE)
    content = models.CharField(max_length=250)
    image = models.ImageField(upload_to='comments/', null=True, blank=True)
    likes = models.ManyToManyField(
        User, blank=True, related_name='comment_likes')
    dislikes = models.ManyToManyField(
        User, blank=True, related_name='comment_dislikes')
    likes_no = models.PositiveIntegerField(default=0)
    dislikes_no = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.author) + "'s comment"
