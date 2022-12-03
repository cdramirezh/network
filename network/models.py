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
            raise ValidationError("A user can't follow themself, that's narcissistic")
    
    def unfollow(self, user):
        """ follower.unfollow(followed) """
        self.following.remove(user)
        self.save()
    
    def get_total_followers(self):
        return self.followers.all().count()

    def get_total_following(self):
        return self.following.all().count()
    

class Post(models.Model):
    content = models.TextField()
    poster = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, related_name="own_posts")
    creation_date = models.DateTimeField(auto_now_add=True)
    
    def like(self, user):
        like = Like(post=self, user=user)
        try: like.clean()
        except: return 0
        like.save()
    
    def unlike(self, user):
        like = Like.objects.filter(post=self, user=user)
        like.delete()

    def get_likes(self):
        return self.likes.all().count()
        # return Like.objects.all().filter(post=self).count()

    def get_posts(type, user=None):
        posts = Post.objects.all().order_by('-creation_date')
        if type == 'ALL': return posts
        if type == 'USER': return posts.filter(poster=user)
        if type == 'FOLLOWING': return posts.filter(poster__in=user.following.all())     

    def __str__(self):
        content_len = len(self.content)
        preview_thresshold = 12
        if content_len >= preview_thresshold:
            content_preview = self.content[0:preview_thresshold] + '...'
        else:
            content_preview = self.content
        format = '%-d/%b/%-y %-H:%M'
        return f'{self.creation_date.strftime(format)} {self.poster}: {content_preview}'

class Like(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(fields = ['post', 'user'], name='oneLikeUserPost')]
        
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='likes')

    def clean(self):
        if Like.objects.filter(post=self.post, user=self.user):
            raise ValidationError({'oneLikeUserPostError':'User already liked this post'})

# Implement only if I can't implement the control on the User model
# or if I can but it's too complicated
# class Follow():
#     follower = models.ForeignKey('User', related_name='undefinded1')
#     followed = models.ForeignKey('User', related_name='unde2')