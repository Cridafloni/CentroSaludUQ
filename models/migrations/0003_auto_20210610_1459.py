# Generated by Django 3.0.6 on 2021-06-10 19:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0002_auto_20210610_1448'),
    ]

    operations = [
        migrations.AddField(
            model_name='entradalote',
            name='eliminado',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='entradalote',
            name='fecha_eliminacion',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='salidalote',
            name='eliminado',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='salidalote',
            name='fecha_eliminacion',
            field=models.DateField(null=True),
        ),
    ]
