# Generated by Django 4.1.1 on 2022-10-02 21:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0004_alter_ad_description_alter_ad_image_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=60, verbose_name='Название категории'),
        ),
    ]
