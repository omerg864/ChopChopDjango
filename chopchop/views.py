from django.shortcuts import render
from django.views.generic import DetailView
from .models import Branch, FoodType, MenuItem, Menu, Settings
from django.template.defaulttags import register
from decimal import *
# Create your views here.

header_url = ""
if len(Settings.objects.all()) > 0:
    settings = Settings.objects.all().first()
    header_url = settings.header_image_url

def home(request):
    branches = Branch.objects.all()
    context = {
        "branches": branches,
        "header_url": header_url,
    }
    return render(request, "home.html", context)


class MenuDetailView(DetailView):
    model = Branch
    template_name = "menu.html"
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        ctx = super(MenuDetailView, self).get_context_data(**kwargs)
        menus_obj = Menu.objects.all().filter(branch=self.get_object()).order_by('index')
        menus = {}
        for m in menus_obj:
            menus[m.name] = {}
            food_types = FoodType.objects.all().filter(branch=m).order_by('index')
            for f in food_types:
                menus[m.name][f.name] = []
                for mi in MenuItem.objects.filter(type1=f).order_by('index'):
                    menus[m.name][f.name].append(mi)
        ctx["menus"] = menus
        ctx["header_url"] = header_url
        return ctx


@register.filter
def fix_number(num):
    return Decimal(num).normalize()
        

@register.filter
def get_attr_key(dictionary, key):
    return dictionary[key]


@register.filter
def get_attr(obj, attri):
    return getattr(obj, attri)


@register.filter
def get_notes_food(key, food):
    menu = Menu.objects.all().filter(name=key).first()
    return FoodType.objects.all().filter(branch=menu, name=food).first().notes


@register.filter
def get_notes_menu(key):
    return Menu.objects.all().filter(name=key).first().notes
