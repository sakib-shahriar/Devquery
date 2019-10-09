from django.http import JsonResponse
from post.models import Vote, CommentVote, Comment
from profilesection.models import Follow
from newsfeed.models import Notification
from django.contrib.auth.models import User
from post.models import Post, Saved
from django.db.models import Q
from django.utils import timesince
from django.urls import reverse
from django.db.models import Count
from django.contrib.staticfiles.templatetags.staticfiles import static
from common.utils.commonUtils import generate_notification


def response(request):
    if request.GET['action'] == 'registration_validation':
        username = request.POST['username']
        email = request.POST['email']
        res = {}
        if User.objects.filter(username=username):
            res['stat'] = "This user name is taken"
        elif User.objects.filter(email=email):
            res['stat'] = "Email already used"
        else:
            res['stat'] = "success"
        return JsonResponse(res)

    if request.GET['action'] == 'plus_vote':
        post_id = request.GET['post_id']
        pVote = Vote.objects.filter(user=request.user, post_id=post_id, vote_direction='plus')
        nVote = Vote.objects.filter(user=request.user, post_id=post_id, vote_direction='minus')
        res = {}
        if nVote.exists():
            nVote.delete()
            post = Post.objects.get(pk=post_id)
            Vote.objects.create(user=request.user, post=post, vote_direction='plus')

            user = User.objects.get(post=post)
            generate_notification(maker=request.user, owner=user, post=post, notf_type="vote",
                                  vote_direction="upvoted")

            res['stat'] = 'swapped'
        elif pVote.exists():
            pVote.delete()
            res['stat'] = 'deleted'
        else:
            post = Post.objects.get(pk=post_id)
            Vote.objects.create(user=request.user, post=post, vote_direction='plus')

            user = User.objects.get(post=post)
            generate_notification(maker=request.user, owner=user, post=post, notf_type="vote",
                                  vote_direction="upvoted")

            res['stat'] = 'created'
        return JsonResponse(res)

    if request.GET['action'] == 'minus_vote':
        post_id = request.GET['post_id']
        pVote = Vote.objects.filter(user=request.user, post_id=post_id, vote_direction='plus')
        nVote = Vote.objects.filter(user=request.user, post_id=post_id, vote_direction='minus')
        res = {}
        if pVote.exists():
            pVote.delete()
            post = Post.objects.get(pk=post_id)
            Vote.objects.create(user=request.user, post=post, vote_direction='minus')

            user = User.objects.get(post=post)
            generate_notification(maker=request.user, owner=user, post=post, notf_type="vote",
                                  vote_direction="downvoted")

            res['stat'] = 'swapped'
        elif nVote.exists():
            nVote.delete()
            res['stat'] = 'deleted'
        else:
            post = Post.objects.get(pk=post_id)
            Vote.objects.create(user=request.user, post=post, vote_direction='minus')

            user = User.objects.get(post=post)
            generate_notification(maker=request.user, owner=user, post=post, notf_type="vote",
                                  vote_direction="downvoted")

            res['stat'] = 'created'
        return JsonResponse(res)

    if request.GET['action'] == 'comment_plus_vote':
        comment_id = request.GET['comment_id']
        pVote = CommentVote.objects.filter(user=request.user, comment_id=comment_id, vote_direction='plus')
        nVote = CommentVote.objects.filter(user=request.user, comment_id=comment_id, vote_direction='minus')
        res = {}
        if nVote.exists():
            nVote.delete()
            comment = Comment.objects.get(pk=comment_id)
            CommentVote.objects.create(user=request.user, comment=comment, vote_direction='plus')

            user = User.objects.get(comment=comment)
            post = Post.objects.get(comment=comment)
            generate_notification(maker=request.user, owner=user, post=post, notf_type="comment_vote",
                                  vote_direction="upvoted")
            res['stat'] = 'swapped'
        elif pVote.exists():
            pVote.delete()
            res['stat'] = 'deleted'
        else:
            comment = Comment.objects.get(pk=comment_id)
            CommentVote.objects.create(user=request.user, comment=comment, vote_direction='plus')

            user = User.objects.get(comment=comment)
            post = Post.objects.get(comment=comment)
            generate_notification(maker=request.user, owner=user, post=post, notf_type="comment_vote",
                                  vote_direction="upvoted")

            res['stat'] = 'created'
        return JsonResponse(res)

    if request.GET['action'] == 'comment_minus_vote':
        comment_id = request.GET['comment_id']
        pVote = CommentVote.objects.filter(user=request.user, comment_id=comment_id, vote_direction='plus')
        nVote = CommentVote.objects.filter(user=request.user, comment_id=comment_id, vote_direction='minus')
        res = {}
        if pVote.exists():
            pVote.delete()
            comment = Comment.objects.get(pk=comment_id)
            CommentVote.objects.create(user=request.user, comment=comment, vote_direction='minus')

            user = User.objects.get(comment=comment)
            post = Post.objects.get(comment=comment)
            generate_notification(maker=request.user, owner=user, post=post, notf_type="comment_vote",
                                  vote_direction="downvoted")

            res['stat'] = 'swapped'
        elif nVote.exists():
            nVote.delete()
            res['stat'] = 'deleted'
        else:
            comment = Comment.objects.get(pk=comment_id)
            CommentVote.objects.create(user=request.user, comment=comment, vote_direction='minus')

            user = User.objects.get(comment=comment)
            post = Post.objects.get(comment=comment)
            generate_notification(maker=request.user, owner=user, post=post, notf_type="comment_vote",
                                  vote_direction="downvoted")

            res['stat'] = 'created'
        return JsonResponse(res)

    if request.GET['action'] == 'search_suggestion':
        text = request.GET['text']
        data = []
        users = User.objects.filter(
            Q(first_name__icontains=text) |
            Q(last_name__icontains=text) |
            Q(username__icontains=text)).distinct()
        for user in users:
            data.append(user.first_name + " " + user.last_name)
        posts = Post.objects.filter(
            Q(title__icontains=text) |
            Q(description__icontains=text)
        ).distinct()
        for post in posts:
            data.append(post.title[:40])
        return JsonResponse(data, safe=False)

    if request.GET['action'] == 'save_post':
        post_id = request.GET['post_id']
        post = Post.objects.get(pk=post_id)
        saved = Saved.objects.filter(post=post, user=request.user)
        res = {}
        if saved.exists():
            saved.delete()
            res['stat'] = "deleted"
        else:
            Saved.objects.create(post=post, user=request.user)
            res['stat'] = "created"
        return JsonResponse(res)

    if request.GET['action'] == 'follow':
        user_id = request.GET['user_id']
        user = User.objects.get(pk=user_id)
        res = {}
        follow = Follow.objects.filter(following=user, follower=request.user)
        if follow.exists():
            follow.delete()
            res['stat'] = 'unfollowed'
        else:
            Follow.objects.create(following=user, follower=request.user)
            generate_notification(maker=request.user, owner=user, post=None, notf_type="follow")
            res['stat'] = 'followed'
        return JsonResponse(res)

    if request.GET['action'] == 'get_notifications':
        notifications = Notification.objects.filter(owner=request.user).order_by('-time')[:7]
        resp = []
        for notification in notifications:
            res = {}
            res['notification'] = notification.notification
            res['id'] = notification.id
            res['name'] = notification.maker.first_name + " " + notification.maker.first_name
            if notification.maker.userinfo.image:
                res['image'] = notification.maker.userinfo.image.url
            else:
                res['image'] = static('img/user.png')
            res['time'] = timesince.timesince(notification.time)
            if notification.is_read:
                res['is_read'] = '1'
            else:
                res['is_read'] = '0'
            if notification.notf_type == "follow":
                res['url'] = reverse('make_read', args=(notification.owner.username, notification.id, "profile"))
            else:
                res['url'] = reverse('make_read', args=(notification.post.id, notification.id, "post"))
            resp.append(res)
        return JsonResponse(resp, safe=False)

    if request.GET['action'] == 'get_notification_num':
        if not request.user.is_authenticated:
            return JsonResponse({'num': 'none'})
        notf_num = Notification.objects.filter(owner=request.user, is_read=False).aggregate(num=Count('id'))['num']
        res = {
            'num': notf_num
        }
        return JsonResponse(res)










