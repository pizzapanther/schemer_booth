from django.db import models

from sorl.thumbnail import get_thumbnail

class Schemer (models.Model):
  name = models.CharField(max_length=255)
  url = models.CharField(max_length=255, blank=True, null=True)
  orig = models.ImageField(upload_to='schemers', blank=True, null=True)
  comp = models.ImageField(upload_to='schemers', blank=True, null=True)
  ts = models.DateTimeField(auto_now_add=True)
  
  def __unicode__ (self):
    return self.name
    
  class Meta:
    ordering = ('-ts',)
    
  def thumbnail (self):
    if self.comp:
      try:
        im = get_thumbnail(self.comp, '128x128')
        return '<img src="%s" alt=""/>' % im.url
        
      except:
        pass
      
    return ''
    
  thumbnail.allow_tags = True
  