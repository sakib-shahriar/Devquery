from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from post.models import Post, Tag, Vote, Comment, CommentVote, Reply, Saved
from django.db.models import Count
from newsfeed.models import Notification
from django.urls import reverse


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
