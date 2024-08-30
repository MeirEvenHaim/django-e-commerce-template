# Generated by Django 5.1 on 2024-08-30 12:52

from django.conf import settings
from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_remove_client_address_remove_client_image_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='user',
            field=models.OneToOneField(
                to=settings.AUTH_USER_MODEL,
                on_delete=models.CASCADE,
                null=True,  # Allow null values temporarily
                blank=True, # Optional: allows the field to be blank in forms
            ),
        ),
        # Optionally, you might want to add a migration step to populate this field
        # with data if needed and then make it non-nullable in a subsequent migration
    ]
