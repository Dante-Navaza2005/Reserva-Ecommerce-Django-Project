# Generated by Django 5.0.3 on 2024-09-01 00:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0009_payment'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='aproved',
            field=models.BooleanField(default=False),
        ),
    ]
