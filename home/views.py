from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from .models import Post
from .forms import PostCreateUpdateForm
from django.utils.text import slugify


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


class PostDeleteView(LoginRequiredMixin, View):
    def get(self, request, post_id):
        post = Post.objects.get(id=post_id)
        if request.user.id == post.user.id:
            post.delete()
            messages.success(request, 'post deleted successfully', 'success')
        else:
            messages.error(request, 'you cant delete this post', 'danger')
        return redirect('home:index')


class PostUpdateView(LoginRequiredMixin, View):
    form_class = PostCreateUpdateForm
    template_name = 'home/update-post.html'

    def setup(self, request, *args, **kwargs):
        self.post_instance = Post.objects.get(pk=kwargs['post_id'])
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        post = self.post_instance
        if not request.user.id == post.user.id:
            messages.error(request, 'You cant update this post', 'danger')
            return redirect('home:index')
        else:
            return super().dispatch(request, *args, **kwargs)

    def get(self, request, post_id):
        post = self.post_instance
        form = self.form_class(instance=post)
        return render(request, self.template_name, {'form': form})

    def post(self, request, post_id):
        post = self.post_instance
        form = self.form_class(request.POST, instance=post)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.slug = slugify(form.cleaned_data['body'][:30])
            new_post.save()
            messages.success(request, 'post updated successfully', 'success')
            return redirect('home:post', post.id, post.slug)


class PostCreateView(View):
    class_form = PostCreateUpdateForm
    template_url = 'home/create-post.html'

    def get(self, request):
        form = self.class_form()
        return render(request, self.template_url, {'form': form})

    def post(self, request):
        form = self.class_form(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.slug = slugify(form.cleaned_data['body'][:30])
            new_post.user = request.user
            new_post.save()
            messages.success(request, 'post created successfully')
            return redirect('home:post', new_post.id, new_post.slug)
