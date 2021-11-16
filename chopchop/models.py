from django.db import models
from django.utils.text import slugify
# Create your models here.


class Branch(models.Model):
    name = models.TextField(default="", verbose_name="Branch name")
    address = models.TextField(default="", blank=True, verbose_name="Address")
    picture = models.TextField(default="", blank=True, verbose_name="Picture Url")
    slug = models.SlugField(max_length=50, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name, allow_unicode=True)
        return super(Branch, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Menu(models.Model):
    name = models.TextField(default="", verbose_name="Name")
    notes = models.TextField(default="", blank=True, verbose_name="notes")
    visible = models.BooleanField(default=True, verbose_name="Can be showed on menu?")
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, verbose_name="Branch Name")
    index = models.PositiveIntegerField(default=0, verbose_name="Number on the menu (optional)")

    def __str__(self):
        return self.name + " - " + self.branch.__str__() + f" ({self.index})"


class FoodType(models.Model):
    name = models.CharField(default="", max_length=200, verbose_name="Starter/main/Desert/pizza...?")
    notes = models.TextField(default="", blank=True, verbose_name="notes")
    branch = models.ForeignKey(Menu, on_delete=models.CASCADE, verbose_name="Menu and Branch")
    index = models.PositiveIntegerField(default=0, verbose_name="Number on the menu (optional)")

    def __str__(self):
        return self.name + ": " + self.branch.__str__() + f" ({self.index})"


class MenuItem(models.Model):
    name = models.TextField(default="", verbose_name="Name")
    description = models.TextField(default="", verbose_name="Description", blank=True)
    price = models.PositiveIntegerField(default=0, verbose_name="Price")
    available = models.BooleanField(default=True, verbose_name="Is available now?")
    visible = models.BooleanField(default=True, verbose_name="Can be showed on menu?")
    type1 = models.ForeignKey(FoodType, on_delete=models.CASCADE, verbose_name="Food type, Menu and Branch")
    index = models.PositiveIntegerField(default=0, verbose_name="Number on the menu (optional)")
    picture_url = models.TextField(default="", blank=True, verbose_name="Picture URL")

    def __str__(self):
        return self.name + " (" + self.type1.__str__() + ")" + f" ({self.index})"

class Settings(models.Model):
    header_image_url = models.TextField(default="", blank=True, verbose_name="Header image URL")

