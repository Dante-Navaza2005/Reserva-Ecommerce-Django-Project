# Generated by Django 5.0.3 on 2024-03-31 11:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_rename_category_categorie'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Adress',
            new_name='Adres',
        ),
        migrations.RenameModel(
            old_name='Categorie',
            new_name='Categoric',
        ),
        migrations.RenameModel(
            old_name='ItemsOrdered',
            new_name='OrderedItem',
        ),
    ]