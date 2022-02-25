from django.shortcuts import render
from django.views.generic import DetailView
from .models import Branch, FoodType, MenuItem, Menu
from .models import Setting as Settings
from django.template.defaulttags import register
from django.contrib.admin.views.decorators import staff_member_required
from decimal import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import HttpResponseRedirect
# Create your views here.

header_url = ""
if len(Settings.objects.all()) > 0:
    settings = Settings.objects.all().first()
    header_url = settings.header_image_url
else:
    settings = Settings(header_image_url="", conversion_rate=120)
    settings.save()

def home(request):
    branches = Branch.objects.all()
    if request.method == 'POST':
        if 'add-branch' in request.POST:
            name = request.POST.get('branch-new')
            address = request.POST.get('branch-address-new')
            picture_url = request.POST.get('branch-picture-new')
            Branch.objects.create(name=name, address=address, picture=picture_url)
            messages.success(request, 'Added New Branch')
            return HttpResponseRedirect(request.path_info)
        else:
            branch_id = request.POST.get("delete-branch")
            branches.filter(id=branch_id).delete()
            messages.success(request, 'Deleted Branch')
            return HttpResponseRedirect(request.path_info)
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
    
    def save(self, request):
        menus_obj = Menu.objects.all().filter(branch=self.get_object()).order_by('index')
        sections = FoodType.objects.all()
        menu_items = MenuItem.objects.all()
        for menu in menus_obj:
            menu.name = request.POST.get(f'menu-{menu.id}')
            menu.index = request.POST.get(f'menu-index-{menu.id}')
            menu.notes = request.POST.get(f'menu-notes-{menu.id}')
            menu.save()
            for section in sections.filter(branch=menu):
                section.name = request.POST.get(f'section-{section.id}')
                section.index = request.POST.get(f'section-index-{section.id}')
                section.notes = request.POST.get(f'section-notes-{section.id}')
                section.save()
                for item in menu_items.filter(type1=section):
                    item.name = request.POST.get(f'item-{item.id}')
                    item.picture_url = request.POST.get(f'item-picture-{item.id}')
                    item.index = request.POST.get(f'item-index-{item.id}')
                    item.description = request.POST.get(f'item-description-{item.id}')
                    item.price = request.POST.get(f'item-price-{item.id}')
                    item.available = checkbox(request.POST.get(f'item-available-{item.id}'))
                    item.save()
    
    def post(self, request, *args, **kwargs):
        self.save(request)
        if 'save' in request.POST:
            messages.success(request, 'Saved Changes')
            return HttpResponseRedirect(request.path_info)
        elif 'delete-section' in request.POST:
            section_id = request.POST.get('delete-section')
            FoodType.objects.all().filter(id=section_id).delete()
            messages.success(request, 'Deleted Food Section and Its Items')
            return HttpResponseRedirect(request.path_info)
        elif 'delete-item' in request.POST:
            item_id = request.POST.get('delete-item')
            MenuItem.objects.all().filter(id=item_id).delete()
            messages.success(request, 'Deleted Menu Item')
            return HttpResponseRedirect(request.path_info)
        elif 'add-section' in request.POST:
            name = request.POST.get('section-new')
            index = request.POST.get('section-new-index')
            menu_id = request.POST.get('add-section')
            menu = Menu.objects.all().get(id=menu_id)
            FoodType.objects.create(name=name, index=index, notes="", branch=menu)
            messages.success(request, 'Added New Food Section')
            return HttpResponseRedirect(request.path_info)
        elif 'add-item' in request.POST:
            section_id = request.POST.get('add-item')
            picture_url = request.POST.get(f'item-picture-new-{section_id}')
            name = request.POST.get(f'item-new-{section_id}')
            index = request.POST.get(f'item-new-index-{section_id}')
            description = request.POST.get(f'item-new-description-{section_id}')
            price = request.POST.get(f'item-new-price-{section_id}')
            section = FoodType.objects.all().get(id=section_id)
            MenuItem.objects.create(name=name, index=index, description=description, price=price, type1=section, picture_url=picture_url, available=True, visible=True)
            messages.success(request, 'Added New Menu Item')
            return HttpResponseRedirect(request.path_info)
        elif 'delete-menu' in request.POST:
            menu_id = request.POST.get('delete-menu')
            Menu.objects.all().filter(id=menu_id).delete()
            messages.success(request, 'Deleted Menu and Its Items')
            return HttpResponseRedirect(request.path_info)
        else:
            print(request.POST)
            name = request.POST.get('menu-new')
            index = request.POST.get('menu-new-index')
            Menu.objects.create(name=name, index=index, visible=True, notes="", branch=self.get_object())
            messages.success(request, 'Added New Menu')
            return HttpResponseRedirect(request.path_info)

def checkbox(string):
    return string == 'on'

@register.filter
def convert_price(dollars):
    settings = Settings.objects.all().first()
    return settings.conversion_rate * dollars


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
