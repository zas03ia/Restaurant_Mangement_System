from django.db import models


class WeekDays(models.TextChoices):
    MONDAY = "MON", "Monday"
    TUESDAY = "TUE", "Tuesday"
    WEDNESDAY = "WED", "Wednesday"
    THURSDAY = "THU", "Thursday"
    FRIDAY = "FRI", "Friday"
    SATURDAY = "SAT", "Saturday"
    SUNDAY = "SUN", "Sunday"


class OrganizationUserRoleChoices(models.TextChoices):
    OWNER = "owner", "Owner"
    ADMIN = "admin", "Admin"
    MANAGER = "manager", "Manager"
    RIDER = "rider", "Rider"
