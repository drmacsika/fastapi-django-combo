from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from .forms import UserAdminChangeForm, UserAdminCreationForm

User = get_user_model()


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    add_form = UserAdminCreationForm
    form = UserAdminChangeForm
    # inlines = [
    #     ProfileInline,
    # ]

    fieldsets = (
        # (None, {'fields': ('password',)}), # This simply shows the hashed password field
        (_('Personal info'), {'fields': ('name', 'email',)}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions',)
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name', 'email', 'password1', 'password2')}
         ),
    )
    list_display = ('id', 'email', 'name', 'is_active', 'is_staff')
    list_display_links = ['email']
    list_filter = ('is_superuser', 'is_staff', 'is_active', 'groups')
    search_fields = ('email', 'name')
    ordering = ('email',)
    list_per_page = 10
    filter_horizontal = ('groups', 'user_permissions',)


admin.site.register(User, UserAdmin)
