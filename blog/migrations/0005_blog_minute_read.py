# Generated by Django 4.0.1 on 2022-07-01 12:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_blog_title_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='minute_read',
            field=models.PositiveIntegerField(default=0, verbose_name='minute to read'),
        ),
    ]
