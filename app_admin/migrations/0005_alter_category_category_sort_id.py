# Generated by Django 4.2.7 on 2024-03-07 08:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_admin', '0004_alter_menu_theme'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='category_sort_id',
            field=models.PositiveIntegerField(unique=True, verbose_name='Toidu kategooria number:'),
        ),
    ]
