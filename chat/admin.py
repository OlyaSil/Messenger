from django.contrib import admin
from .models import GroupChat, Message, UserProfile

class GroupChatAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    filter_horizontal = ('members',)

class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'group', 'content', 'timestamp')
    search_fields = ('sender__username', 'group__name', 'content')
    list_filter = ('timestamp',)

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio')
    search_fields = ('user__username', 'bio')

admin.site.register(GroupChat, GroupChatAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
