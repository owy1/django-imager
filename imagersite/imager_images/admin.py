"""Add admin tools."""


from django.contrib import admin
from imager_images.models import Photo, Album


# Register your models here.
class ImageAdmin(admin.ModelAdmin):
    """Display images with descriptions."""

    list_display = ('title', 'user', 'published')
    list_filter = ('user',)

admin.site.register(Photo, ImageAdmin)
admin.site.register(Album, ImageAdmin)
