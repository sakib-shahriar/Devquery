from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from post.models import Post, Tag, Vote, Comment, CommentVote, Reply, Saved
from django.db.models import Count
from newsfeed.models import Notification
from django.urls import reverse
from datetime import datetime
from django.contrib.auth.models import User
from common.utils.commonUtils import generate_notification


class PostView(TemplateView):
    template_name = 'post/post.html'

    def get(self, request, post_id, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('index')
        post = Post.objects.get(pk=post_id)
        pVote = Vote.objects.filter(post=post, vote_direction='plus').aggregate(num=Count('id'))['num']
        nVote = Vote.objects.filter(post=post, vote_direction='minus').aggregate(num=Count('id'))['num']
        comments = Comment.objects.filter(post=post)
        tags = Tag.objects.filter(post=post)
        replies, cpVotes, cnVotes, voted = [], [], [], []
        myVote = None
        saved = False
        if Vote.objects.filter(post=post, user=request.user):
            myVote = Vote.objects.filter(post=post, user=request.user).first()
        if Saved.objects.filter(post=post, user=request.user):
            saved = True
        for comment in comments:
            replies.append(Reply.objects.filter(comment=comment))
            cpVotes.append(CommentVote.objects.filter(comment=comment, vote_direction="plus").
                           aggregate(num=Count('id'))['num'])
            cnVotes.append(CommentVote.objects.filter(comment=comment, vote_direction="minus").
                           aggregate(num=Count('id'))['num'])
            try:
                voted.append(CommentVote.objects.get(comment=comment, user=request.user))
            except CommentVote.DoesNotExist:
                voted.append(None)
        context = {
            'post': post,
            'pVote': pVote,
            'nVote': nVote,
            'comments': zip(comments, replies, cpVotes, cnVotes, voted),
            'tags': tags,
            'myVote': myVote,
            'saved': saved
        }
        return render(request, self.template_name, context)


class MakeReadView(TemplateView):
    def get(self, request, id, notification_id, t, *args, **kwargs):
        notification = Notification.objects.get(pk=notification_id)
        notification.is_read = True
        notification.save()
        if t == "post":
            url = reverse('post', args=(id,))
        else:
            url = reverse('profile', args=(id,))
        return redirect(url)


class CommentView(TemplateView):
    template_name = 'partials/post/_comment.html'

    def get(self, request, *args, **kwargs):
        comment = request.GET['comment']
        post_id = request.GET['post_id']
        post = Post.objects.get(pk=post_id)
        comment = Comment.objects.create(comment=comment, time=datetime.now(), post=post, user=request.user)
        comment.save()
        user = User.objects.get(post=post)
        generate_notification(maker=request.user, owner=user, post=post, notf_type="comment")
        cpVote = CommentVote.objects.filter(comment=comment, vote_direction="plus").aggregate(num=Count('id'))['num']
        cnVote = CommentVote.objects.filter(comment=comment, vote_direction="minus").aggregate(num=Count('id'))['num']
        replies = Reply.objects.filter(comment=comment)
        try:
            voted = CommentVote.objects.get(comment=comment, user=request.user)
        except CommentVote.DoesNotExist:
            voted = None
        context = {'comment': comment, 'replies': replies, 'cpvVote': cpVote, 'cnVote': cnVote, 'voted': voted}
        return render(request, self.template_name, context)


class ReplyView(TemplateView):
    template_name = 'partials/post/_reply.html'

    def get(self, request, *args, **kwargs):
        comment_id = request.GET['comment_id']
        reply = request.GET['reply']
        comment = Comment.objects.get(pk=comment_id)
        reply = Reply.objects.create(comment=comment, reply=reply, time=datetime.now(), user=request.user)
        user = User.objects.get(comment=comment)
        post = Post.objects.get(comment=comment)
        generate_notification(maker=request.user, owner=user, post=post, notf_type="reply")
        context = {'reply': reply}
        return render(request, self.template_name, context)

