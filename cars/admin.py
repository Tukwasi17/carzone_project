from django.contrib import admin
from cars.models import Car
from django.utils.html import format_html

# Register your models here.
class CarAdmin(admin.ModelAdmin):
    def thumbnail(self, object):#to display picture
        return format_html('<img src="{}" width="40" style="border-radius: 50px;" />'.format(object.car_photo.url))
    
    thumbnail.short_description = 'Car Image'#changing the name thumbnail to photo
    
    list_display = ('id', 'thumbnail', 'car_title', 'city', 'color', 'model', 'year', 'body_style', 'fuel_type', 'is_featured')
    list_display_links = ('id', 'thumbnail', 'car_title')#to be clickable
    list_editable = ('is_featured',)#editing auto
    search_fields = ('id', 'car_title', 'city', 'model', 'body_style', 'fuel_type')
    list_filter = ('city', 'model', 'body_style', 'fuel_type')


admin.site.register(Car, CarAdmin)