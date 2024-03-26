from django.urls import path
from . import views

urlpatterns = [
    path('SignIn/', views.SignIn, name='SignIn'),
    path('SignUp/', views.SignUp, name='SignUp'),
    path('profile/<int:esport>/', views.profile, name='profile'),
    path('logout/', views.logout, name='logout'),
    path('settings/', views.settings, name='settings'),
    path('', views.List_of_Posts, name='List_of_Posts'),
    path('post/create/', views.Created_Post, name='Created_Post'),
    path('post/<int:esport>/delete/', views.Deleted_Post, name='Deleted_Post'),
    path('post/<int:esport>/update/', views.Updated_Post, name='Updated_Post'),
    path('post/<int:esport>/', views.Post_Details, name='Post_Details'),
]
