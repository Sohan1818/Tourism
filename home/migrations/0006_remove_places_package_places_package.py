# Generated by Django 4.1.5 on 2023-04-10 12:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_places'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='places',
            name='package',
        ),
        migrations.AddField(
            model_name='places',
            name='package',
            field=models.ManyToManyField(to='home.package'),
        ),
    ]
