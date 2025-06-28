# admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomAccounts, UserProfile, BrandProfile

class CustomAccountsAdmin(UserAdmin):
    model = CustomAccounts
    list_display = ("email", "first_name", "last_name", "is_staff", "is_superuser")
    list_filter = ("is_staff", "is_superuser", "is_brandowner")
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal Info", {"fields": ("first_name", "last_name", "username")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "is_brandowner", "groups", "user_permissions")}),
        ("Important dates", {"fields": ("last_login",)}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "first_name", "last_name", "password1", "password2"),
        }),
    )
    search_fields = ("email",)
    ordering = ("email",)


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "address", "state", "city", "dob")


class BrandProfileAdmin(admin.ModelAdmin):
    list_display = ("owner", "brand_name", "username", "address", "id")

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "owner":
            kwargs["queryset"] = CustomAccounts.objects.filter(is_brandowner=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(CustomAccounts, CustomAccountsAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(BrandProfile, BrandProfileAdmin)
