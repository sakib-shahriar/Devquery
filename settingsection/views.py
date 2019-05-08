from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from post.models import Post, Tag, Vote, Comment, Saved
from profilesection.models import Follow, UserInfo
from django.contrib.auth.models import User
from profilesection.models import  Interest
from django.db.models import Q, Count
from datetime import datetime
from account.choices import tags
from django.contrib import messages


class SettingView(TemplateView):
    template_name = 'settingsection/setting.html'

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        interest = Interest.objects.filter(user=request.user)
        my_tags = []
        for tag in interest:
            my_tags.append(tag.tag)
        context = {
            'my_tags': my_tags,
            'tags': tags,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        first_name = request.POST['first-name']
        last_name = request.POST['last-name']
        tags = request.POST.getlist('tags[]')
        image = request.FILES.get('image', False)
        profile_tag = request.POST['profile-tag']
        about = request.POST['about']
        location = request.POST['location']
        portfolio = request.POST['portfolio']
        user = request.user
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        userinfo = UserInfo.objects.get(user=user)
        userinfo.profile_tag = profile_tag
        userinfo.about = about
        userinfo.location = location
        userinfo.portfolio = portfolio
        if image:
            userinfo.image = image
        userinfo.save()
        interest = Interest.objects.filter(user=user)
        interest.delete()
        for tag in tags:
            Interest.objects.create(user=user, tag=tag)
        messages.add_message(request, messages.SUCCESS, "Changed saved successfully")
        return redirect('index')

