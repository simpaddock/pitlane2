# Generated by Django 2.1.2 on 2019-03-16 09:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='race',
            old_name='Race',
            new_name='Session',
        ),
    ]