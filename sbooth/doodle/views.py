import os
import base64
import datetime
from PIL import Image
import cStringIO

from django import http
from django.conf import settings
from django.template.response import TemplateResponse
from django.core.files import File
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.shortcuts import get_object_or_404
from django.views.generic import ListView

from .models import Schemer

TACHE_PATH = os.path.join(settings.PPATH, 'doodle', 'static', 'doodle', 'facehair.png')

def home (request):
  message = ''
  
  if request.method == 'POST':
    name = request.POST.get('name', '')
    url = request.POST.get('url', '')
    imgdata = request.POST.get('imgdata', '')
    coord = request.POST.get('coord', '220,330')
    
    if name:
      if imgdata:
        imgdata = base64.b64decode(imgdata)
        fh = cStringIO.StringIO(imgdata)
        img = Image.open(fh)
        
        try:
          img.load()
          
        except:
          message = 'Invalid Image'
          
        else:
          fh.seek(0)
          s = Schemer(name=name)
          if url:
            s.url = url
            
          s.save()
          fn = datetime.datetime.now().strftime('schemers/%Y%m%d_%H%M%S%f')
          
          path = default_storage.save(fn + '.png', ContentFile(fh.read()))
          s.orig = fn + '.png'
          s.save()
          
          img = Image.open(s.orig.path)
          logo = Image.open(TACHE_PATH)
          
          coord = coord.split(',')
          offset = (int(coord[0]), int(coord[1]))
          
          logo = logo.convert("RGBA")
          r,g,b,a = logo.split()
          img.paste(logo, offset, mask=a)
          
          out = cStringIO.StringIO()
          img.save(out, "PNG")
          out.seek(0)
          path = default_storage.save(fn + '_comp.png', ContentFile(out.read()))
          s.comp = fn + '_comp.png'
          s.save()
          out.close()
          fh.close()
          
          return http.HttpResponseRedirect('/photos/%d/' % s.id)
          
        fh.close()
        
      else:
        message = 'Missing an Image'
        
    else:
      message = 'Missing a Name'
      
  c = {'message': message}
  return TemplateResponse(request, 'home.html', c)
  
def photo (request, sid):
  c = {'schemer': get_object_or_404(Schemer, id=sid)}
  return TemplateResponse(request, 'photo.html', c)
  
class Photos (ListView):
  queryset = Schemer.objects.all()
  context_object_name = "schemers"
  paginate_by = 2
  template_name = 'photos.html'
  