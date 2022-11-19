from django.contrib import admin
from .models import User, Post, Like

class PostInlineAdmin(admin.TabularInline):
    # Through lets me reference the model that manages the many to many relationship
    model = Like

class UserAdmin(admin.ModelAdmin):
    fields = ['password', 'username', 'email', 'following']
    inlines = [PostInlineAdmin,]

class PostAdmin(admin.ModelAdmin):
    fields = ['content', 'poster',]
    inlines = [PostInlineAdmin,]

# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Post, PostAdmin)