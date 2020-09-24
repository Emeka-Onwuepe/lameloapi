# Generated by Django 3.0.2 on 2020-09-24 08:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='customerId',
        ),
        migrations.AddField(
            model_name='customer',
            name='address',
            field=models.CharField(default='address', max_length=256, verbose_name='address'),
            preserve_default=False,
        ),
    ]
