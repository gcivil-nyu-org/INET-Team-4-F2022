from django.contrib import admin
from .models import News, newsComment


class NewsAdmin(admin.ModelAdmin):
    list_display = ("title", "desc", "img", "url")
    search_fields = ["title", "desc", "img", "url"]


admin.site.register(News, NewsAdmin)


@admin.register(newsComment)
class newsCommentAdmin(admin.ModelAdmin):
    list_display = ("content", "post", "created_on", "active")
    list_filter = ("active", "created_on")
    search_fields = ("user", "content")
    actions = ["approve_comments"]

    def approve_comments(self, request, queryset):
        queryset.update(active=True)
