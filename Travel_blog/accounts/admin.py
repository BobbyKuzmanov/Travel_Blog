from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from django.contrib import messages
from Travel_blog.accounts.models import Profile
from Travel_blog.accounts.groups import create_admin_groups
from django.db.models.signals import post_migrate

UserModel = get_user_model()


class ProfileInlineAdmin(admin.StackedInline):
    model = Profile
    verbose_name_plural = 'Profile'


# Unregister the default User admin
admin.site.unregister(UserModel)


@admin.register(UserModel)
class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInlineAdmin,)
    list_display = ('username', 'email', 'is_staff', 'is_superuser', 'get_groups')
    actions = ['make_staff', 'make_superadmin', 'remove_staff']

    def get_groups(self, obj):
        return ", ".join([group.name for group in obj.groups.all()])

    get_groups.short_description = 'Groups'

    def make_staff(self, request, queryset):
        try:
            staff_group = Group.objects.get(name='Staff')
            for user in queryset:
                if not user.is_staff:
                    user.is_staff = True
                    user.groups.add(staff_group)
                    user.save()
            messages.success(request, f'Successfully added {queryset.count()} users to Staff group')
        except Group.DoesNotExist:
            messages.error(request, 'Staff group does not exist. Please run create_admin_groups first.')

    make_staff.short_description = "Add selected users to Staff group"

    def make_superadmin(self, request, queryset):
        try:
            superadmin_group = Group.objects.get(name='SuperAdmin')
            for user in queryset:
                if not user.is_superuser:
                    user.is_superuser = True
                    user.is_staff = True
                    user.groups.add(superadmin_group)
                    user.save()
            messages.success(request, f'Successfully added {queryset.count()} users to SuperAdmin group')
        except Group.DoesNotExist:
            messages.error(request, 'SuperAdmin group does not exist. Please run create_admin_groups first.')

    make_superadmin.short_description = "Add selected users to SuperAdmin group"

    def remove_staff(self, request, queryset):
        for user in queryset:
            if not user.is_superuser:  # Prevent removing staff status from superusers
                user.is_staff = False
                user.groups.clear()
                user.save()
        messages.success(request, f'Successfully removed staff status from {queryset.count()} users')

    remove_staff.short_description = "Remove staff status from selected users"


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'email')
    search_fields = ('user__username', 'first_name', 'last_name', 'email')
    readonly_fields = ('user',)


# Create admin groups if they don't exist
def create_groups(app_config, **kwargs):
    create_admin_groups()


post_migrate.connect(create_groups)
