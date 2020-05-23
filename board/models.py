from django.db import models
from django.contrib.auth.models import User

from .fields import CustomIntegerField


class Post(models.Model):
    title = models.CharField(max_length=120)
    url = models.URLField(default="localhost")
    creation_date = models.DateTimeField(auto_now_add=True)
    upvotes = CustomIntegerField(min_value=0, max_value=100, default=0)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="comment"
    )
    parent = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="children",
    )

    class Meta:
        ordering = ["id"]


class Upvote(models.Model):
    ip = models.GenericIPAddressField()
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="post_upvote"
    )

    def __str__(self):
        return self.post.title
