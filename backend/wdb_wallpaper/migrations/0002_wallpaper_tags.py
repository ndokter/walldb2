# Generated by Django 5.1.5 on 2025-01-25 08:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wdb_wallpaper', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='wallpaper',
            name='tags',
            field=models.ManyToManyField(blank=True, null=True, to='wdb_wallpaper.tag'),
        ),
    ]
