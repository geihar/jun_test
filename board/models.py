from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

from .fields import CustomIntegerField


class Post(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField()
    content = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)


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
