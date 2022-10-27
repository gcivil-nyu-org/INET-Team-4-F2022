from django.contrib import admin
from .models import Post, Comment

class PostAdmin(admin.ModelAdmin):
    list_display = ('title','created_on')
    #list_filter = ("status",)
    search_fields = ['title', 'content']
    #prepopulated_fields = {'slug': ('title',)}

admin.site.register(Post, PostAdmin)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('content', 'post', 'created_on', 'active')
    list_filter = ('active', 'created_on')
    search_fields = ('user', 'content')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(active=True)
