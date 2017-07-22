"""Docstring for superuser."""

from django.contrib import admin
from imager_profile.models import ImagerProfile

# Register your models here.


class UserAdmin(admin.ModelAdmin):
    """Display users with descriptions."""

    list_display = ('user', 'photography_style', 'social_status')
    list_filter = ('user',)

admin.site.register(ImagerProfile, UserAdmin)
