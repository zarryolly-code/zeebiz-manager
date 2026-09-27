from django.db import models
from django.contrib.auth.models import User


class Business(models.Model):
    owner = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="business"
    )

    name = models.CharField(
        max_length=200
    )

    tagline = models.CharField(
        max_length=255,
        blank=True
    )

    description = models.TextField(
        blank=True
    )

    logo = models.ImageField(
        upload_to="business_logos/",
        blank=True,
        null=True
    )

    primary_color = models.CharField(
        max_length=7,
        default="#1F4E79"
    )

    secondary_color = models.CharField(
        max_length=7,
        default="#F59E0B"
    )

    email = models.EmailField(
        blank=True
    )

    phone = models.CharField(
        max_length=30,
        blank=True
    )

    address = models.TextField(
        blank=True
    )

    website = models.URLField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.name