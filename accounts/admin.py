from django.contrib import admin


from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Role

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Role

class CustomUserAdmin(UserAdmin):
    list_display = ['email', 'username', 'created_at']  # Keep 'created_at' here since it's for display only
    list_filter = ['roles']
    search_fields = ['email', 'username']
    ordering = ['email']

    # Remove 'created_at' from fieldsets (because it’s non-editable)
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Roles', {'fields': ('roles',)}),  # Keep roles editable
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),  # Exclude 'created_at' from editable fields
    )

    # You can include 'created_at' in list_display but not in the editable fields
    readonly_fields = ['created_at']  # If you want to display it as a read-only field in the admin

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'roles')}
        ),
    )

    filter_horizontal = ('roles', 'groups', 'user_permissions',)

# Register CustomUser with the admin site
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Role)



'''
class CustomUserAdmin(UserAdmin):
    list_display = ['email', 'username', 'created_at']  # You can add more fields here
    list_filter = ['roles']  # This allows filtering users by their roles
    search_fields = ['email', 'username']
    ordering = ['email']
    
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Roles', {'fields': ('roles',)}),  # Add the roles field to the form
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined', 'created_at')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'roles')}
        ),
    )
    filter_horizontal = ('roles', 'groups', 'user_permissions',)  # Makes role selection easier in the admin

# Register models in the admin
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Role)
'''


'''
# Register your models here.
from django.contrib import admin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_moderator', 'is_data_collector', 'is_feedback_contributor', 'is_admin', 'created_at')
    search_fields = ('username', 'email')
    list_filter = ('is_moderator', 'is_data_collector', 'is_feedback_contributor', 'is_admin')

    def save_model(self, request, obj, form, change):
        """
        Allow only custom admins to assign the 'is_moderator' and 'is_feedback_contributor' roles.
        """
        if request.user.is_admin or request.user.is_superuser:  # Only allow admins or superusers to modify roles
            super().save_model(request, obj, form, change)
        else:
            raise PermissionDenied("You do not have permission to assign these roles.")
'''

