from django.urls import path, include
from . import views

app_name = 'home'
urlpatterns = [
    path('', views.HomeView.as_view(), name='index'),
    path('post/<int:post_id>/<slug:post_slug>', views.PostDetailView.as_view(), name='post'),
    path('post/<int:post_id>', views.PostDeleteView.as_view(), name='delete-post'),
]