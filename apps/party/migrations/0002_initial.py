# Generated by Django 4.2.4 on 2023-10-22 19:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("party", "0001_initial"),
        ("tournaments", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="party",
            name="tournament",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="tournaments.tournament"
            ),
        ),
    ]
