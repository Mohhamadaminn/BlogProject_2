from django.urls import path
from .views import PostListView, PostDetailView, PostCreateView
from .views import PostUpdateView, PostDeleteView, user_profile
from . import views
from django.http import HttpResponse


urlpatterns = [
    path('posts/', PostListView.as_view(), name='posts_list'),
    path('create/', PostCreateView.as_view(), name='post_create'),
    path('user/edit/', views.edit_profile, name='edit_profile'),
    path('user/<str:username>/', views.user_profile, name='user_profile'),
    path('<slug>/edit/', PostUpdateView.as_view(), name='post_update'),
    path('<slug:slug>/', PostDetailView.as_view(), name='post_detail'),
    path('<slug>/delete/', PostDeleteView.as_view(), name='post_delete'),
]
