# Generated by Django 4.2.3 on 2023-10-27 10:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resume', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='experience',
            name='end_date',
            field=models.DateField(blank=True, default=None, null=True),
        ),
    ]
