from django.contrib import admin
from .models import User, Post

class PostInlineAdmin(admin.TabularInline):
    # Through lets me reference the model that manages the many to many relationship
    model = Post.likers.through

class UserAdmin(admin.ModelAdmin):
    fields = ['password', 'username', 'email']
    inlines = [PostInlineAdmin]

# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Post)