# Generated by Django 3.2.9 on 2022-10-15 12:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0024_user_user_generate_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='expiration_date',
            field=models.TimeField(blank=True, null=True),
        ),
    ]
