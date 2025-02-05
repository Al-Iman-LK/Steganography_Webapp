from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, UserProfile
from .forms import CustomUserCreationForm, CustomUserChangeForm

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ('username', 'email', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ()}),  # Removed 'bio' as it is not a field in UserProfile
    )

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_files_processed', 'storage_used', 'created_at')
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('created_at',)
