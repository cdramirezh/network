from email.policy import default
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    content = models.TextField()
    poster = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, related_name="own_posts")
    creation_date = models.DateTimeField(auto_now_add=True)

    likers = models.ManyToManyField('User', blank=True, related_name="liked_posts")
    # test if I this is inmutable. I need it to be mutable
    likes = models.PositiveIntegerField(default=0, editable=True)
    def like(self, user):
        self.likers.aaggregate(user)
        self.likes += 1
        self.save()
    
    def unlike(self, user):
        self.likers.remove(user)
        self.likes -= 1
        self.save()

    def __str__(self):
        content_len = len(self.content)
        preview_thresshold = 12
        if content_len >= preview_thresshold:
            content_preview = self.content[0:preview_thresshold] + '...'
        else:
            content_preview = self.content
        format = '%-d/%b/%-y %-H:%M'
        return f'{self.creation_date.strftime(format)} {self.poster}: {content_preview}'
    
    def clean(self):
        if self.likers.count() != self.likes:
            raise ValidationError(f'Something went wrong. Likers: {self.likers.count()} Likes: {self.likes}')

# Implement only if I can't implement the control on the User model
# or if I can but it's too complicated
# class Follow():
#     pass