# Generated by Django 4.1.1 on 2022-10-02 21:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_rename_myuser_user_rename_log_location_lng'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='location',
            new_name='location_id',
        ),
    ]
