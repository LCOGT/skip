# Generated by Django 3.1 on 2021-04-28 16:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('skip', '0007_auto_20210427_1820'),
    ]

    operations = [
        migrations.RenameField(
            model_name='alert',
            old_name='event',
            new_name='events',
        ),
    ]
