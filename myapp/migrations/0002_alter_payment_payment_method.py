# Generated by Django 5.1 on 2024-09-01 18:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='payment_method',
            field=models.CharField(choices=[('Credit Card', 'Credit Card'), ('PayPal', 'PayPal')], default='PayPal', max_length=20),
        ),
    ]
