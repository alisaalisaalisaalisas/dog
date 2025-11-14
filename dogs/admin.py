from django.contrib import admin
from .models import Dog


@admin.register(Dog)
class DogAdmin(admin.ModelAdmin):
    list_display = ("name", "breed", "age", "gender", "owner", "created_at")
    list_filter = ("gender", "breed")
    search_fields = ("name", "breed")
