# Generated by Django 3.1 on 2020-10-21 00:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('skip', '0004_auto_20201021_0010'),
    ]

    operations = [
        migrations.RenameField(
            model_name='alert',
            old_name='message_extras',
            new_name='extracted_fields',
        ),
    ]
