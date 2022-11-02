from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models


class User(AbstractUser):
    following = models.ManyToManyField('User', blank=True, related_name='followers')

    def follow(self, user):
        """ follower.follow(followed) """
        if user != self:
            self.following.add(user)
            self.save()
        else:
            raise ValidationError("A user can't follow themself, that's narcissist")
    
    def unfollow(self, user):
        """ follower.unfollow(followed) """
        self.following.remove(user)
        self.save()
    
    def clean(self):
        if self in self.following.all():
            self.following.remove(self)
            raise ValidationError("A user can't follow themself, that's narcissist")

class Post(models.Model):
    content = models.TextField()
    poster = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, related_name="own_posts")
    creation_date = models.DateTimeField(auto_now_add=True)

    likers = models.ManyToManyField('User', blank=True, related_name="liked_posts")
    def like(self, user):
        self.likers.add(user)
        self.save()
    
    def unlike(self, user):
        self.likers.remove(user)
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
    
# Implement only if I can't implement the control on the User model
# or if I can but it's too complicated
# class Follow():
#     follower = models.ForeignKey('User', related_name='undefinded1')
#     followed = models.ForeignKey('User', related_name='unde2')