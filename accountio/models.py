from django.db import models
from shared.models import BaseModel
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import gettext_lazy as _
from .choices import WeekDays, OrganizationUserRoleChoices


# Create your models here.
class Location(BaseModel):
    name = models.CharField(max_length=255, verbose_name=_("Location Name"))
    address = models.CharField(max_length=255, verbose_name=_("Address"))
    city = models.CharField(max_length=100, verbose_name=_("City"))
    state = models.CharField(
        max_length=100, verbose_name=_("State"), null=True, blank=True
    )
    postal_code = models.CharField(max_length=20, verbose_name=_("Postal Code"))
    country = models.CharField(max_length=100, verbose_name=_("Country"))

    def __str__(self):
        return f"{self.name}, {self.city}, {self.country}"


class Organization(BaseModel):
    name = models.CharField(max_length=255, verbose_name=_("Organization Name"))
    domain = models.CharField(max_length=20, null=True, blank=True)
    description = models.TextField()
    vat = models.IntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100),
        ],  # VAT in percentage
        verbose_name=_("VAT Percentage"),
    )

    locations = models.ManyToManyField(
        "Location", related_name="organizations", verbose_name=_("Locations")
    )

    start_week_day = models.CharField(
        max_length=3, choices=WeekDays.choices, verbose_name=_("Start Week Day")
    )

    end_week_day = models.CharField(
        max_length=3, choices=WeekDays.choices, verbose_name=_("End Week Day")
    )

    start_time = models.TimeField(verbose_name=_("Start Time"))
    end_time = models.TimeField(verbose_name=_("End Time"))

    def __str__(self):
        return f"{self.name}, {self.domain}"
