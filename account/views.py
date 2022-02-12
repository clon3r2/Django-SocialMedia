from django.shortcuts import render
from django.views import View
from django.shortcuts import render, redirect
from .forms import UserRegistrationForm
from django.contrib.auth.models import User
from django.contrib import messages


class RegisterView(View):
    template_name = 'account/register.html'

    def get(self, request):
        form = UserRegistrationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            clean_data = form.cleaned_data
            User.objects.create_user(clean_data['username'], clean_data['email'], clean_data['password'])
            messages.success(request, 'you registered successfully', 'success')
            return redirect('home:index')
        else:
            return render(request, self.template_name, {'form': form})
