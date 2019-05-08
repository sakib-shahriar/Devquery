from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    title = models.CharField(max_length=255, default="")
    description = models.TextField()
    image = models.ImageField(upload_to='photos/postimg')
    time = models.DateTimeField(auto_now=True, auto_now_add=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Tag(models.Model):
    name = models.CharField(max_length=20)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('post', 'name'),)

    def __str__(self):
        return self.post


class Comment(models.Model):
    comment = models.TextField()
    time = models.DateTimeField(auto_now=True, auto_now_add=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.post


class Saved(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('post', 'user'),)

    def __str__(self):
        return self.post


class Vote(models.Model):
    vote_direction = models.CharField(max_length=10)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('post', 'user'),)

    def __str__(self):
        return self.vote_direction


class CommentVote(models.Model):
    vote_direction = models.CharField(max_length=10)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('comment', 'user', 'vote_direction'),)

    def __str__(self):
        return self.comment


class Reply(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reply = models.TextField()
    time = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.comment







