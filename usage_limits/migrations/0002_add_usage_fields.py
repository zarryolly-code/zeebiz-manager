from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("usage_limits", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="usagecounter",
            name="quotation_count",
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name="usagecounter",
            name="quotation_year",
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name="usagecounter",
            name="quotation_month",
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name="usagecounter",
            name="invoice_count",
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name="usagecounter",
            name="invoice_year",
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name="usagecounter",
            name="invoice_month",
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name="usagecounter",
            name="receipt_count",
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name="usagecounter",
            name="receipt_year",
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name="usagecounter",
            name="receipt_month",
            field=models.PositiveIntegerField(default=0),
        ),
    ]