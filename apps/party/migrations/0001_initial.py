# Generated by Django 4.2.4 on 2023-10-22 19:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Party",
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
                ("start_time", models.DateTimeField(blank=True, null=True)),
                ("is_full", models.BooleanField(default=False)),
                ("is_closed", models.BooleanField(default=False)),
                (
                    "creator",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="users.player",
                    ),
                ),
                (
                    "players",
                    models.ManyToManyField(
                        blank=True, related_name="parties", to="users.player"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="PartyParticipant",
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
                    "status",
                    models.CharField(
                        choices=[
                            ("pending", "Pending"),
                            ("confirmed", "confirmed"),
                            ("declined", "declined"),
                        ],
                        default="pending",
                        max_length=10,
                    ),
                ),
                (
                    "party",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="party.party"
                    ),
                ),
                (
                    "player",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="users.player"
                    ),
                ),
            ],
        ),
    ]
