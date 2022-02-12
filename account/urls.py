from django.urls import path, include
from . import views

app_name = 'account'
urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='index')
]
