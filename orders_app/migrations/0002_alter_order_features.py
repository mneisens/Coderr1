# Generated by Django 5.2.3 on 2025-06-11 19:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='features',
            field=models.JSONField(blank=True, default=list),
        ),
    ]
