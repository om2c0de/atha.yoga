# Generated by Django 4.1.4 on 2022-12-27 20:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "courses",
            "0006_rename_skip_lessons_amount_coursecycle_canceled_lessons_amount_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="course",
            name="rate",
            field=models.FloatField(default=5),
        ),
    ]
