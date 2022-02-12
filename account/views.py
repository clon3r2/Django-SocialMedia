from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.shortcuts import render, redirect
from .forms import UserRegistrationForm, UserLoginForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from home.models import Post

class UserRegisterView(View):
    template_name = 'account/register.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:index')
        else:
            return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = UserRegistrationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            clean_data = form.cleaned_data
            User.objects.create_user(clean_data['username'], clean_data['email'], clean_data['password1'])
            messages.success(request, 'you registered successfully', 'success')
            return redirect('home:index')
        else:
            return render(request, self.template_name, {'form': form})


class UserLoginView(View):
    form_class = UserLoginForm
    template_name = 'account/login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:index')
        else:
            return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            clean_data = form.cleaned_data
            user = authenticate(request, username=clean_data['username'], password=clean_data['password'])
            if user is not None:
                login(request, user)
                messages.success(request, 'you logged in successfully', 'success')
                return redirect('home:index')
            else:
                messages.success(request, 'username or password is not correct', 'warning')
        return render(request, self.template_name, {'form': form})


class UserLogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.success(request, "you've been logged out successfully", 'success')
        return redirect('home:index')


class UserProfileView(LoginRequiredMixin, View):
    template_name = 'account/user_profile.html'

    def get(self, request, user_id):
        user = User.objects.get(pk=user_id)
        posts = Post.objects.filter(user=user)
        return render(request, self.template_name, {'user': user, 'posts': posts})