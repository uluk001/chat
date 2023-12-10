from django.contrib import admin
from .models import CustomUser


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'is_staff', 'is_active', 'is_superuser', 'last_login', 'date_joined')
    list_display_links = ('id', 'username')
    search_fields = ('username', 'email')


admin.site.register(CustomUser, CustomUserAdmin)
