from django.shortcuts import render
from django.views.generic import DetailView
from .models import Branch, FoodType, MenuItem, Menu, Settings
from django.template.defaulttags import register
from django.contrib.admin.views.decorators import staff_member_required
from decimal import *
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.

header_url = ""
if len(Settings.objects.all()) > 0:
    settings = Settings.objects.all().first()
    header_url = settings.header_image_url
else:
    settings = Settings(header_image_url="")
    settings.save()

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
        ctx["sections"] = FoodType.objects.all()
        ctx["menu_items"] = MenuItem.objects.all()
        ctx["menus"] = menus_obj
        ctx["header_url"] = header_url
        return ctx

class EditView(LoginRequiredMixin, DetailView):
    model = Branch
    template_name = "edit.html"
    slug_url_kwarg = 'slug'


    def get_context_data(self, **kwargs):
        ctx = super(EditView, self).get_context_data(**kwargs)
        menus_obj = Menu.objects.all().filter(branch=self.get_object()).order_by('index')
        ctx["sections"] = FoodType.objects.all()
        ctx["menu_items"] = MenuItem.objects.all()
        ctx["menus"] = menus_obj
        ctx["header_url"] = header_url
        return ctx
    
    def post(self, request, *args, **kwargs):
        print("yes")


@register.filter
def get_section_items(section):
    return MenuItem.objects.all().filter(type1=section).order_by('index')

@register.filter
def get_menu_sections(menu):
    return FoodType.objects.all().filter(branch=menu).order_by('index')

@register.filter
def get_menu_id(menu_ids, index):
    return menu_ids[index]

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
