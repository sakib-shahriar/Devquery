from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from post.models import Post, Tag, Vote, Comment, Saved
from profilesection.models import Follow
from django.contrib.auth.models import User
from profilesection.models import  Interest
from django.db.models import Q, Count
from datetime import datetime


class ProfileView(TemplateView):
    template_name = 'profilesection/profile.html'

    def get(self, request, username, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        user = User.objects.get(username=username)
        interest = Interest.objects.filter(user=user)
        follower = Follow.objects.filter(following=user).aggregate(num=Count('id'))['num']
        following = Follow.objects.filter(follower=user).aggregate(num=Count('id'))['num']
        posts = Post.objects.filter(user=user).order_by('-time')
        user_following = False
        if Follow.objects.filter(follower=request.user, following=user):
            user_following = True
        pVotes, nVotes, tags, comments, voted, saved = [], [], [], [], [], []
        for post in posts:
            pVotes.append(Vote.objects.filter(post=post).filter(vote_direction='plus').
                          aggregate(num=Count('id'))['num'])
            nVotes.append(Vote.objects.filter(post=post).filter(vote_direction='minus').
                          aggregate(num=Count('id'))['num'])
            comments.append(Comment.objects.filter(post=post).aggregate(num=Count('id'))['num'])
            tags.append(Tag.objects.filter(post=post))
            try:
                voted.append(Vote.objects.get(post=post, user=request.user))
            except Vote.DoesNotExist:
                voted.append(None)
            try:
                saved.append(Saved.objects.get(post=post, user=request.user))
            except Saved.DoesNotExist:
                saved.append(None)

        context = {
            'usr': user,
            'posts': zip(posts, pVotes, nVotes, comments, tags, voted, saved),
            'interest': interest,
            'follower': follower,
            'following': following,
            'user_following': user_following,
        }
        return render(request, self.template_name, context)
