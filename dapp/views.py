from django.shortcuts import render_to_response
from django.http import HttpResponse
#from adv_web.models import posts
from models import Duplex_products

def acad(request):
    entries = Duplex_products.objects.all()[1:2] ## so only get one item from database
    return render_to_response('acad.html',{'duplexes':entries})

def home(request):
    entries = Duplex_products.objects.all()[:10]
    return render_to_response('index.html',{'duplexes':entries})



