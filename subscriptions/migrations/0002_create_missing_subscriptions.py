from django.db import migrations


def create_missing_subscriptions(apps, schema_editor):
    Business = apps.get_model("businesses", "Business")
    Subscription = apps.get_model("subscriptions", "Subscription")

    for business in Business.objects.all():
        Subscription.objects.get_or_create(
            business=business,
            defaults={
                "plan": "Free",
                "is_active": True,
            },
        )


class Migration(migrations.Migration):

    dependencies = [
        ("subscriptions", "0001_initial"),
        ("businesses", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(create_missing_subscriptions),
    ]