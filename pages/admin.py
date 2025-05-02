from django.contrib import admin
from .models import Team
from django.utils.html import format_html

# Register your models here.

class TeamAdmin(admin.ModelAdmin):
    def thumbnail(self, object):#to display photo
        return format_html('<img src="{}" width="40" style="border-radius: 50px;" />'.format(object.photo.url))
    
    thumbnail.short_description = 'Photo' #changing the name thumbnail to photo

    list_display = ('id', 'thumbnail', 'first_name', 'designation', 'created_date')#using Tuple
    list_display_links = ('id', 'thumbnail', 'first_name')# to be clickable
    search_fields = ('first_name', 'last_name', 'designation')
    list_filter = ('designation',)

admin.site.register(Team, TeamAdmin)