from django.urls import path
from . import views

urlpatterns = [
    path('SignIn/', views.SignIn, name='SignIn'),
    path('SignUp/', views.SignUp, name='SignUp'),
    path('profile/<int:pk>/', views.profile, name='profile'),
    path('logout/', views.LogOut, name='logout'),
    path('settings/', views.View_Settings, name='Settings'),
    path('', views.List_of_Posts, name='List_of_Posts'),
    path('post/create/', views.Created_Post, name='Created_Post'),
    path('post/<int:pk>/delete/', views.Deleted_Post, name='Deleted Post'),
    path('post/<int:pk>/update/', views.Updated_Post, name='Updated Post'),
    path('post/<int:pk>/', views.Post_Details, name='Post_Details'),
    path('post/<str:pk>/comment/', views.Commented, name='Commented'),
    path('comment/<int:comment_id>/delete/', views.delete_comment,
         name='delete_comment'),
]
