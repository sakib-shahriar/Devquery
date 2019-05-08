from django.db import models
from django.contrib.auth.models import User
from post.models import Tag


class Follow(models.Model):
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following_user')
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower_user')

    class Meta:
        unique_together = (('following', 'follower'),)

    def __str__(self):
        return self.following


class Interest(models.Model):
    tag = models.CharField(max_length=20)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('tag', 'user'),)

    def __str__(self):
        return self.tag


class Skill(models.Model):
    skill = models.CharField(max_length=25)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user


class UserInfo(models.Model):
    image = models.ImageField(upload_to='photos/userimg', blank=True)
    profile_tag = models.CharField(max_length=50)
    location = models.CharField(max_length=100)
    about = models.CharField(max_length=150)
    github = models.CharField(max_length=100)
    stackoverflow = models.CharField(max_length=100)
    facebook = models.CharField(max_length=100)
    twitter = models.CharField(max_length=100)
    portfolio = models.CharField(max_length=100)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user




