# Generated by Django 5.0.6 on 2024-07-03 19:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Auth_App', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tempuser',
            name='mobile_Number',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
