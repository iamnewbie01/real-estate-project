# Generated by Django 5.1.1 on 2024-11-03 18:20

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("members", "0002_remove_property_available_from_propertyimage"),
    ]

    operations = [
        migrations.AlterField(
            model_name="propertyimage",
            name="image",
            field=models.ImageField(upload_to="property_images/%Y/%m/%d/"),
        ),
    ]