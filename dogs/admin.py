from django.contrib import admin
from .models import Dog, UserProfile, Match, Message, Favorite


@admin.register(Dog)
class DogAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "breed",
        "age",
        "gender",
        "size",
        "owner",
        "is_active",
        "created_at",
    )
    list_filter = ("gender", "size", "breed", "is_active", "looking_for")
    search_fields = ("name", "breed", "owner__username")
    list_editable = ("is_active",)
    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        (
            "Основная информация",
            {"fields": ("owner", "name", "breed", "age", "gender", "size")},
        ),
        (
            "Характеристики",
            {"fields": ("temperament", "looking_for", "description", "photo")},
        ),
        ("Настройки", {"fields": ("is_active",)}),
        ("Даты", {"fields": ("created_at", "updated_at"), "classes": ("collapse",)}),
    )


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "location", "phone", "created_at")
    list_filter = ("location", "created_at")
    search_fields = ("user__username", "user__email", "location")
    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        ("Пользователь", {"fields": ("user",)}),
        ("Персональная информация", {"fields": ("bio", "location", "phone", "avatar")}),
        ("Даты", {"fields": ("created_at", "updated_at"), "classes": ("collapse",)}),
    )


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ("dog_from", "dog_to", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = (
        "dog_from__name",
        "dog_to__name",
        "dog_from__owner__username",
        "dog_to__owner__username",
    )
    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        ("Мэтч", {"fields": ("dog_from", "dog_to", "status")}),
        ("Даты", {"fields": ("created_at", "updated_at"), "classes": ("collapse",)}),
    )


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("sender", "receiver", "subject", "is_read", "created_at")
    list_filter = ("is_read", "created_at")
    search_fields = ("sender__username", "receiver__username", "subject", "content")
    readonly_fields = ("created_at",)

    fieldsets = (
        ("Отправитель", {"fields": ("sender",)}),
        ("Получатель", {"fields": ("receiver",)}),
        ("Сообщение", {"fields": ("subject", "content", "is_read")}),
        ("Дата", {"fields": ("created_at",), "classes": ("collapse",)}),
    )


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ("user", "dog", "created_at")
    list_filter = ("created_at",)
    search_fields = ("user__username", "dog__name", "dog__breed")
    readonly_fields = ("created_at",)

    fieldsets = (
        ("Пользователь", {"fields": ("user",)}),
        ("Собака", {"fields": ("dog",)}),
        ("Дата", {"fields": ("created_at",), "classes": ("collapse",)}),
    )
