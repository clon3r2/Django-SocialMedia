from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    name = models.CharField(max_length=200)
    slug = models.SlugField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.slug} - {self.created}'

    def get_absolute_url(self):
        return reverse('home:post', args=[self.id, self.slug])

    class Meta:
        ordering = ['-created']


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='UserComments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='PostComments')
    body = models.TextField()
    reply = models.ForeignKey('self', on_delete=models.CASCADE, related_name='ReplyComments', blank=True, null=True)
    is_reply = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} - {self.body[:30]}'

