# Generated by Django 3.1.1 on 2020-10-25 21:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proyecto', '0002_auto_20201015_1221'),
    ]

    operations = [
        migrations.AddField(
            model_name='ratiosempresa',
            name='año',
            field=models.IntegerField(default=2011),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='ratiosempresa',
            unique_together={('codEmpresa', 'codRatio', 'año')},
        ),
    ]