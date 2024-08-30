# Generated by Django 5.1 on 2024-08-30 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_rename_user_client_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='client',
            old_name='User',
            new_name='user',
        ),
        migrations.AlterField(
            model_name='client',
            name='role',
            field=models.CharField(choices=[('admin', 'Admin'), ('employee', 'Employee'), ('client', 'Client')], default='user', max_length=20),
        ),
    ]
