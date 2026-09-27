from django.db import models
from django.contrib.auth.models import User
from businesses.models import Business


class Customer(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    business = models.ForeignKey(
        Business,
        on_delete=models.CASCADE,
        related_name="customers",
    )

    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name