from django.contrib import admin

from .models import Schemer

class SAdmin (admin.ModelAdmin):
  list_display = ('name', 'url', 'ts', 'thumbnail')
  search_fields = ('name', 'url')
  
admin.site.register(Schemer, SAdmin)
