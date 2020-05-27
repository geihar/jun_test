from django.contrib import admin

from .models import Post, Comment, Upvote


admin.site.register(Comment)
admin.site.register(Upvote)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "author")
    search_fields = ("title", "body")
    prepopulated_fields = {"slug": ("title",)}
