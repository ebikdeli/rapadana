# Generated by Django 4.0.1 on 2022-01-17 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='end',
            field=models.DateField(blank=True, null=True, verbose_name='project end time(est)'),
        ),
        migrations.AlterField(
            model_name='order',
            name='price',
            field=models.DecimalField(decimal_places=0, default=-1, max_digits=12, verbose_name='price'),
        ),
        migrations.AlterField(
            model_name='order',
            name='start',
            field=models.DateField(blank=True, null=True, verbose_name='project start date'),
        ),
    ]
