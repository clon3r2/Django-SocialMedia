from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from .models import Post

class HomeView(View):
    template_name = 'home/index.html'

    def get(self, request):
        posts = Post.objects.all()
        return render(request, self.template_name, {'posts': posts})

    def post(self, request):
        pass


class PostDetailView(View):
    template_name = 'home/post.html'

    def get(self, request, post_id, post_slug):
        post = Post.objects.get(pk=post_id, slug=post_slug)
        return render(request, self.template_name, {'post': post})
