# Generated by Django 3.0.6 on 2021-07-06 23:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0005_auto_20210610_1703'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lote',
            name='eliminado',
            field=models.BooleanField(default=True, verbose_name='En lista'),
        ),
    ]