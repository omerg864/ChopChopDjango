from django.contrib import admin
from .models import MenuItem, Branch, FoodType, Menu
from .models import Setting as Settings

# Register your models here.


class BranchAdmin(admin.ModelAdmin):
    fields = ("name", "address", "picture")


admin.site.register(Branch, BranchAdmin)
admin.site.register(Menu)
admin.site.register(FoodType)
admin.site.register(MenuItem)
admin.site.register(Settings)

