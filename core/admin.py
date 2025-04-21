from django.contrib import admin

from core.models import Message, Room, RoomMember


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ("name", "owner", "is_private", "created_at")
    search_fields = ("name", "description")
    list_filter = ("is_private", "created_at")
    ordering = ("-created_at",)


@admin.register(RoomMember)
class RoomMemberAdmin(admin.ModelAdmin):
    list_display = ("user", "room", "is_online", "joined_at")
    search_fields = ("user__username", "room__name")
    list_filter = ("is_online", "joined_at")
    ordering = ("-joined_at",)
    raw_id_fields = ("user", "room")
    autocomplete_fields = ("user", "room")


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("author", "room", "status", "created_at")
    search_fields = ("content", "author__username", "room__name")
    list_filter = ("status", "created_at")
    ordering = ("-created_at",)
    raw_id_fields = ("room", "author")
    autocomplete_fields = ("room", "author")
