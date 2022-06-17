from django.contrib import admin

from .models import User


@admin.register(User)
class GenreAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'username', 'first_name',
        'last_name', 'email', 'role'
    )
