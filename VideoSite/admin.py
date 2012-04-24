from VideoSite.models import *
from django.contrib import admin

class CommentInline(admin.StackedInline):
    model = Comment

class LinkInline(admin.StackedInline):
    model = Link

class VideoAdmin(admin.ModelAdmin):
    fieldsets = [
    (None, {'fields': ['name', 'eventTime', 'description', 'sport', 'videoLocation', 'rating']}),
    ]
    inlines = [CommentInline]
    list_filter = ('uploadTime', 'eventTime')
    search_fields = ['name']

class SportAdmin(admin.ModelAdmin):
    inlines = [LinkInline]

admin.site.register(Video, VideoAdmin)
admin.site.register(Sport, SportAdmin)
