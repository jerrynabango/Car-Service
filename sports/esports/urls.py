from django.urls import path
from . import views

urlpatterns = [
    path('signin/', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('profile/<int:esport>/', views.profile, name='profile'),
    path('logout/', views.logout, name='logout'),
    path('settings/', views.settings, name='settings'),
    path('', views.post_list, name='post_list'),
    path('post/create/', views.post_create, name='post_create'),
    path('post/<int:esport>/delete/', views.post_delete, name='post_delete'),
    path('post/<int:esport>/update/', views.post_update, name='post_update'),
    path('post/<int:esport>/', views.post_detail, name='post_detail'),
]
