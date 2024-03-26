from django.urls import path
from . import views

urlpatterns = [
    path('SignIn/', views.SignIn, name='SignIn'),
    path('SignUp/', views.SignUp, name='SignUp'),
    path('profile/<int:esport>/', views.profile, name='Profile'),
    path('logout/', views.LogOut, name='logout'),
    path('settings/', views.View_Settings, name='Settings'),
    path('', views.List_of_Posts, name='List of Posts'),
    path('post/create/', views.Created_Post, name='Created_Post'),
    path('post/<int:esport>/delete/', views.Deleted_Post, name='Deleted Post'),
    path('post/<int:esport>/update/', views.Updated_Post, name='Updated Post'),
    path('post/<int:esport>/', views.Post_Details, name='Post Details'),
]
