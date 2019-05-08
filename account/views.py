from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth.models import User
from profilesection.models import Interest, UserInfo
from account.choices import tags
from django.contrib import auth, messages


class LoginView(TemplateView):
    template_name = 'account/login.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index')
        return render(request, self.template_name)

    def post(self, request):
        username = request.POST['user-name']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('index')
        else:
            messages.add_message(request, messages.ERROR, "Username or password did not match")
            return redirect('login')


class RegisterView(TemplateView):
    template_name = 'account/register.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index')
        context = {'tags': tags}
        return render(request, self.template_name, context)

    def post(self, request):
        first_name = request.POST['first-name']
        last_name = request.POST['last-name']
        username = request.POST['user-name']
        email = request.POST['email']
        password = request.POST['password']
        tags = request.POST.getlist('tags[]')
        image = request.FILES.get('image', False)
        user = User.objects.create_user(username=username, email=email, first_name=first_name,
                                        last_name=last_name, password=password)
        for tag in tags:
            Interest.objects.create(tag=tag, user=user)
        if image:
            UserInfo.objects.create(image=image, user=user, profile_tag="user")
        else:
            UserInfo.objects.create(user=user, profile_tag="user")
        return redirect('login')


class Logout(TemplateView):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            auth.logout(request)
            return redirect('login')
        return redirect('index')
