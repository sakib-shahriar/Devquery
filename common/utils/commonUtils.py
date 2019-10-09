from newsfeed.models import Notification
from datetime import datetime
from django.contrib.auth.models import User
from post.models import Post


def generate_notification(maker, owner, post, notf_type, vote_direction=""):
    if notf_type == "follow":
        notification = maker.first_name + " " + maker.last_name + " has started to follow you"
        post = Post.objects.all().first()
        Notification.objects.create(notification=notification, time=datetime.now(), is_read=False, owner=owner,
                                    maker=maker, post=post, notf_type=notf_type)

    elif notf_type == "reply":
        if maker == owner:
            return
        post_owner = User.objects.get(post=post)
        if post_owner == owner:
            post_owner = "your"
        else:
            post_owner = post_owner.first_name + " " + post_owner.last_name + "'s"
        notification = maker.first_name + " " + maker.last_name + " replied to your comment in " + post_owner + " post"
        Notification.objects.create(notification=notification, time=datetime.now(), is_read=False, owner=owner,
                                    maker=maker, post=post, notf_type=notf_type)

    elif notf_type == "comment":
        if maker == owner:
            return
        notification = maker.first_name + " " + maker.last_name + " commented on your post"
        Notification.objects.create(notification=notification, time=datetime.now(), is_read=False, owner=owner,
                                    maker=maker, post=post, notf_type=notf_type)

    elif notf_type == "comment_vote":
        if maker == owner:
            return
        post_owner = User.objects.get(post=post)
        if post_owner == owner:
            post_owner = "your"
        else:
            post_owner = post_owner.first_name + " " + post_owner.last_name + "'s"
        notification = maker.first_name + " " + maker.last_name + " " + vote_direction + " your comment in " + post_owner + " post"
        Notification.objects.create(notification=notification, time=datetime.now(), is_read=False, owner=owner,
                                    maker=maker, post=post, notf_type=notf_type)

    if notf_type == "vote":
        if maker == owner:
            return
        notification = maker.first_name + " " + maker.last_name + " " + vote_direction + " your post"
        Notification.objects.create(notification=notification, time=datetime.now(), is_read=False, owner=owner,
                                    maker=maker, post=post, notf_type=notf_type)