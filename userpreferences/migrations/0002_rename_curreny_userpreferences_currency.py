# Generated by Django 5.0.2 on 2024-03-03 12:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userpreferences', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userpreferences',
            old_name='curreny',
            new_name='currency',
        ),
    ]