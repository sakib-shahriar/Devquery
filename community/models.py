from django.db import models
from django.contrib.auth.models import User
from post.models import Post


class Community(models.Model):
    title = models.CharField(max_length=20)
    details = models.TextField()

    def __str__(self):
        return self.title


class CommunityPost(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, unique=True)
    community = models.ForeignKey(Community, on_delete=models.CASCADE)

    def __str__(self):
        return self.community


class CommunityFollower(models.Model):
    community = models.ForeignKey(Community, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('community', 'user'),)

    def __str__(self):
        return self.community
