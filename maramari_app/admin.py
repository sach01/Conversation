from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import SentencePair

# Register your models here.
# admin.site.register(SentencePair)

# maramari_app/admin.py

from django.contrib import admin
from .models import (
    User,
    Language,
    Dialect,
    UserProfile,
    Badge,
    Achievement,
    Notification,
    SentencePair,
    TranslateSentence
)
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        (None, {'fields': ('created_at',)}),
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'created_at')

admin.site.register(Language)
admin.site.register(Dialect)
admin.site.register(UserProfile)
admin.site.register(Badge)
admin.site.register(Achievement)
admin.site.register(Notification)
admin.site.register(SentencePair)
admin.site.register(TranslateSentence)

