from django.db import models
from shared.models import BaseModel
from accountio.models import Organization


# Create your models here.
class Menu(BaseModel):
    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name="menus"
    )
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name


class Category(BaseModel):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name="categories")
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Item(BaseModel):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="items"
    )
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    quantity = models.IntegerField(default=0)
    modifiers = models.ManyToManyField("Modifier", related_name="items", blank=True)

    def __str__(self):
        return self.name


class Modifier(BaseModel):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name
