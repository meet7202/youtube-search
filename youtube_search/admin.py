from django.contrib import admin

from .models import YoutubeVideo, Tag


class YTVideoAdmin(admin.ModelAdmin):
    list_display = ('id', 'video', 'published_at', 'title', 'description', 'thumb_url',)
    search_fields = ('id', 'video', 'published_at', 'title', 'description', 'key_words__name',)
    list_filter = ("description", "key_words")

class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    search_fields = ('id', 'name',)
    list_filter = ("id", "name")

admin.site.register(Tag)
admin.site.register(YoutubeVideo, YTVideoAdmin)
