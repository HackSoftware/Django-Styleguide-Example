# Generated by Django 4.1.3 on 2022-11-28 11:58

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("common", "0004_remove_randommodel_start_date_before_end_date_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="SimpleModel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        db_index=True, default=django.utils.timezone.now
                    ),
                ),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.AddField(
            model_name="randommodel",
            name="simple_objects",
            field=models.ManyToManyField(
                blank=True, related_name="random_objects", to="common.simplemodel"
            ),
        ),
    ]
