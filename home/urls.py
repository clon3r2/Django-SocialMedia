from django.urls import path, include
from . import views

app_name = 'home'
urlpatterns = [
    path('', views.HomeView.as_view(), name='index'),
    path('post/<int:post_id>/<slug:post_slug>', views.PostDetailView.as_view(), name='post'),
    path('post/delete/<int:post_id>', views.PostDeleteView.as_view(), name='delete-post'),
    path('post/update/<int:post_id>', views.PostUpdateView.as_view(), name='update-post'),
    path('post/create/', views.PostCreateView.as_view(), name='create-post'),
]