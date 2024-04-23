# Generated by Django 4.2.10 on 2024-02-14 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("news_app", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Headline",
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
                ("title", models.CharField(max_length=200)),
                ("image", models.URLField(blank=True, null=True)),
                ("url", models.TextField()),
            ],
        ),
    ]