# Generated by Django 4.2.7 on 2024-01-29 08:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_admin', '0002_alter_fooditem_food'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='prepared',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='menu',
            name='recommends',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='menu',
            name='theme',
            field=models.CharField(blank=True, default='TEEMAPÄEV:', max_length=50, null=True),
        ),
    ]
