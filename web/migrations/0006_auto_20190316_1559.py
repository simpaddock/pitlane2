# Generated by Django 2.1.2 on 2019-03-16 14:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0005_category_textblock_upload'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lap',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Position', models.IntegerField()),
                ('Duration', models.FloatField()),
            ],
        ),
        migrations.AddField(
            model_name='driverresult',
            name='Driver',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='web.Driver'),
            preserve_default=False,
        ),
        migrations.RemoveField(
            model_name='driverresult',
            name='Laps',
        ),
        migrations.AddField(
            model_name='driverresult',
            name='Laps',
            field=models.ManyToManyField(to='web.Lap'),
        ),
    ]
