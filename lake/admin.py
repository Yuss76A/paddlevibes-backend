from django.contrib import admin
from .models import Lake, Photo, Review


class LakeAdmin(admin.ModelAdmin):
    list_display = ('name', 'latitude', 'longitude')
    search_fields = ('name',)


class PhotoAdmin(admin.ModelAdmin):
    list_display = ('lake', 'description')
    search_fields = ('lake__name',)


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('lake', 'user', 'rating', 'comment')
    search_fields = ('lake__name', 'user__name')
    list_filter = ('rating',)


admin.site.register(Lake, LakeAdmin)
admin.site.register(Photo, PhotoAdmin)
admin.site.register(Review, ReviewAdmin)
