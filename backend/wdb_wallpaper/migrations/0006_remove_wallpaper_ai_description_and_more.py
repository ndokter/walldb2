# Generated by Django 5.1.5 on 2025-01-26 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wdb_wallpaper', '0005_wallpaper_ai_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wallpaper',
            name='ai_description',
        ),
        migrations.AddField(
            model_name='wallpaper',
            name='chromadb_description',
            field=models.TextField(blank=True, help_text='Description of image to make searchable with ChromaDB', null=True),
        ),
    ]
