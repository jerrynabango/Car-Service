from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.conf import settings


# Create your models here.
class User(AbstractUser):
    profile_picture = models.ImageField(upload_to='profile_pictures/',
                                        blank=True, null=True,
                                        default='default_profile_picture.jpg')
    User_Bio = models.TextField(blank=True, null=True)

    class Meta:
        # Add this to avoid table name conflicts
        db_table = 'custom_user'

    # Add related_name for groups and user_permissions
    groups = models.ManyToManyField(Group, related_name='esports_users')
    user_permissions = models.ManyToManyField(Permission,
                                              related_name='esports_users')

    def __str__(self):
        return self.username


class Comment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE,
                             related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE)
    text = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.author.username} on {self.post.title}'


class Post(models.Model):
    Title = models.CharField(max_length=200)
    Author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE)
    Content = models.TextField()
    Created = models.DateTimeField(auto_now_add=True)
    Updated = models.DateTimeField(auto_now=True)
    Views = models.IntegerField(default=0)

    def __str__(self):
        return self.title
