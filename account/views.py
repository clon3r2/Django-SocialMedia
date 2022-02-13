from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserRegistrationForm, UserLoginForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import views as auth_views
from .models import Relation


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
        is_following = False
        user = get_object_or_404(User, pk=user_id)
        relation = Relation.objects.filter(from_user=request.user, to_user=user)
        if relation.exists():
            is_following = True
        posts = user.posts.all()
        return render(request, self.template_name, {'user': user, 'posts': posts, 'is_following': is_following})


class UserPasswordResetView(auth_views.PasswordResetView):
    template_name = 'account/password_reset_form.html'
    success_url = reverse_lazy('account:password_reset_done')
    email_template_name = 'account/password_reset_email.html'


class UserPasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'account/password_reset_done.html'


class UserPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'account/password_reset_confirm.html'
    success_url = reverse_lazy('account:password_reset_complete')


class UserPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'account/password_reset_complete.html'


class UserFollowingView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        target_user = User.objects.get(id=user_id)
        relation = Relation.objects.filter(from_user=request.user, to_user=target_user)
        if relation.exists():
            messages.error(request, 'you already have this guy on ur followings.', 'danger')
        else:
            Relation(from_user=request.user, to_user=target_user).save()
            messages.success(request, 'you followed this guy successfully.', 'success')
        return redirect('account:profile', target_user.id)


class UserUnFollowingView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        target_user = User.objects.get(id=user_id)
        relation = Relation.objects.filter(from_user=request.user, to_user=target_user)
        if relation.exists():
            relation.delete()
            messages.success(request, 'you unfollowed this guy', 'success')
        else:
            messages.error(request, 'you have not this user in ur followings', 'danger')
        return redirect('account:profile', target_user.id)

