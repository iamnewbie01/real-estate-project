# Generated by Django 5.1.1 on 2024-11-04 01:21

import members.models
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("members", "0003_alter_propertyimage_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="propertyimage",
            name="image",
            field=models.ImageField(upload_to=members.models.property_image_upload_to),
        ),
    ]
