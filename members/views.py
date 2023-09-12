from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
# Create your views here.
# Import model 
from .models import Member

#index 
def index(request):
    template = loader.get_template('main.html')
    return HttpResponse(template.render())

#get all member templates
def members(request):
    mymembers = Member.objects.all().values()
    template = loader.get_template('all_members.html')
    context = {
        'mymembers': mymembers
    }
    return HttpResponse(template.render(context, request))

#get detail of members
def details(request, id): 
    mymember = Member.objects.get(id=id)
    template = loader.get_template('details.html')
    context = {
        'mymember': mymember
    }
    return HttpResponse(template.render(context, request))

#get detail with slug 
def slugs(request, slug):
    mymember = Member.objects.get(slug=slug)
    template = loader.get_template('details.html')
    context = {
        'mymember': mymember
    }
    return HttpResponse(template.render(context, request))

def testing(request):
    members = Member.objects.all().values()
    template = loader.get_template('template.html')
    context = {
        'firstname': 'Linus',
        'mymembers': members,
        'members':members,
        'fruits': ['Apple', 'Banana', 'Cherry', 'Orange'],
        'mycar': {
            'brand': 'Ford',
            'model': 'Mustang',
            'year': '1964',
        },
        'greeting': 1,
        'day': 'Friday',
         'x': ['Apple', 'Banana', 'Cherry'], 
         'y': ['Apple', 'Banana', 'Cherry'], 
    }
    return HttpResponse(template.render(context, request))