# Generated by Django 3.2 on 2021-05-12 19:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0002_auto_20210510_1552'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='num_followers',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='account',
            name='num_following',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
