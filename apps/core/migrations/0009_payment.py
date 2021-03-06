# Generated by Django 4.0.1 on 2022-02-22 10:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_alter_customer_address_alter_customer_email_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=0, default=-1, max_digits=12, verbose_name='amount')),
                ('time', models.DateTimeField(auto_now_add=True, verbose_name='time')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='core.order')),
            ],
        ),
    ]
