# Generated by Django 4.1.4 on 2022-12-26 20:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0005_transaction_status"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="first_name",
            field=models.CharField(
                blank=True, max_length=100, verbose_name="first name"
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="last_name",
            field=models.CharField(
                blank=True, max_length=100, verbose_name="last name"
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="pwd_reset_token",
            field=models.CharField(
                blank=True, max_length=300, null=True, verbose_name="pwd reset token"
            ),
        ),
    ]
