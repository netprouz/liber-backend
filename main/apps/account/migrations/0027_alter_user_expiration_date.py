# Generated by Django 3.2.9 on 2022-10-18 19:46

from django.db import migrations, models
import main.apps.account.models.user


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0026_alter_user_expiration_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='expiration_date',
            field=models.CharField(blank=True, default=main.apps.account.models.user.user_expire_time, max_length=100, null=True),
        ),
    ]
