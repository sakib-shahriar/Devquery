from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from post.models import Post, Tag, Vote, Comment, Saved
from profilesection.models import Interest, Follow
from datetime import datetime
from django.contrib import messages
from newsfeed.models import Notification
from django.contrib.auth.models import User
from django.db.models import Q
from django.utils import timesince
from django.urls import reverse
from django.db.models import Count
from django.contrib.staticfiles.templatetags.staticfiles import static


class MainView(TemplateView):
    template_name = 'newsfeed/index.html'

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')

        following = Follow.objects.filter(follower=request.user)
        interest = Interest.objects.filter(user=request.user)
        posts = Post.objects.filter(
            Q(user__following_user__in=following) |
            Q(tag__name__in=interest.values('tag')) |
            Q(user=request.user)
        ).distinct().order_by('-time')

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
            'posts': zip(posts, pVotes, nVotes, comments, tags, voted, saved),
        }
        return render(request, self.template_name, context)


class CreatePostView(TemplateView):
    template_name = 'newsfeed/create-post.html'

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if request.user.is_authenticated:
            return render(request,self.template_name)

    def post(self, request):
        title = request.POST['title']
        description = request.POST['description']
        image = request.FILES.get('image', False)
        tag = request.POST['tag']
        if image:
            post = Post.objects.create(title=title, description=description, image=image,
                                       time=datetime.now(), user=request.user)
            post.save()
        else:
            post = Post.objects.create(title=title, description=description, time=datetime.now(), user=request.user)
            post.save()
        tag = tag.split(",")
        for t in tag:
            Tag.objects.create(name=t, post=post)
        messages.add_message(request, messages.SUCCESS, "Posted successfully")
        return redirect('index')


class SearchView(TemplateView):
    template_name = 'newsfeed/search.html'

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        key = request.GET['key']
        key_components = key.split(" ")
        users = []
        cnt = 0
        for component in key_components:
            if cnt == 0:
                if component != "":
                    users = User.objects.filter(
                        Q(first_name__icontains=component) |
                        Q(last_name__icontains=component) |
                        Q(username__icontains=component)).filter(is_superuser=False).distinct()
            else:
                if component != "":
                    users = users | User.objects.filter(
                        Q(first_name__icontains=component) |
                        Q(last_name__icontains=component) |
                        Q(username__icontains=component)).filter(is_superuser=False).distinct()
            cnt = cnt + 1

        users = users.distinct()

        posts = Post.objects.filter(
            Q(title__icontains=key) |
            Q(description__icontains=key)
        ).distinct()
        context = {
            "users": users,
            "posts": posts
        }
        messages.add_message(request, messages.INFO, "Showing search result for "+key)
        return render(request, self.template_name, context)


class SavedView(TemplateView):
    template_name = 'newsfeed/saved.html'

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        saved = Saved.objects.filter(user=request.user)
        posts = []
        for sv in saved:
            posts.append(Post.objects.get(pk=sv.post.id))
        context = {
            "posts": posts
        }
        return render(request, self.template_name, context)


class TagPostView(TemplateView):
    template_name = 'newsfeed/index.html'

    def get(self, request, name, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')

        posts = Post.objects.filter(tag__name=name)
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
            'posts': zip(posts, pVotes, nVotes, comments, tags, voted, saved),
        }
        messages.add_message(request, messages.INFO, "Showing all posts including "+name+" tag")
        return render(request, self.template_name, context)


class NotificationView(TemplateView):
    template_name = 'newsfeed/notification.html'

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        notifications = Notification.objects.filter(owner=request.user).order_by('-time')[:50]
        context = {
            'notifications': notifications
        }
        return render(request, self.template_name, context)


class NotificationPopupView(TemplateView):
    template_name = 'partials/_notification.html'

    def get(self, request, *args, **kwargs):
        notifications = Notification.objects.filter(owner=request.user).order_by('-time')[:7]
        urls = []
        for notification in notifications:
            if notification.notf_type == "follow":
                urls.append(reverse('make_read', args=(notification.owner.username, notification.id, "profile")))
            else:
                urls.append(reverse('make_read', args=(notification.post.id, notification.id, "post")))

        context = {'notifications': zip(notifications, urls)}
        return render(request, self.template_name, context if notifications else {})
