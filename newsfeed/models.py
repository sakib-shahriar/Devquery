from django.db import models
from django.contrib.auth.models import User
from post.models import Post


class Notification(models.Model):
    notification = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    maker = models.ForeignKey(User, on_delete=models.CASCADE, related_name='maker_user')
    time = models.DateTimeField(auto_now=False, auto_now_add=True)
    notf_type = models.CharField(max_length=25, default="")
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.notification
