# Generated by Django 3.2 on 2021-05-09 21:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100)),
                ('nickname', models.CharField(blank=True, max_length=100, null=True)),
                ('bio', models.CharField(blank=True, max_length=300, null=True)),
                ('average_likes', models.IntegerField(blank=True, null=True)),
                ('num_followers', models.IntegerField()),
                ('num_following', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Connection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('connection_type', models.CharField(max_length=20)),
                ('fro', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fro_connections', to='network.account')),
                ('to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to_connections', to='network.account')),
            ],
        ),
    ]
