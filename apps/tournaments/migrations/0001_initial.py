# Generated by Django 4.2.4 on 2023-10-22 19:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("users", "0001_initial"),
        ("courses", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="PlayerParticipation",
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
                    "player",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="users.player"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Tournament",
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
                ("name", models.CharField(max_length=100)),
                ("start_date", models.DateField()),
                ("end_date", models.DateField()),
                (
                    "game_type",
                    models.CharField(
                        choices=[
                            ("match play", "match play"),
                            ("stroke play", "stroke play"),
                            ("nassau", "Nassau"),
                        ],
                        default="stroke play",
                        max_length=50,
                    ),
                ),
                (
                    "hole_selection",
                    models.CharField(
                        choices=[
                            ("18", "18"),
                            ("F9", "F9"),
                            ("B9", "Back 9"),
                            ("custom", "Custom"),
                        ],
                        default="full 18",
                        max_length=10,
                    ),
                ),
                ("custom_holes", models.CharField(blank=True, max_length=100)),
                (
                    "course",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="courses.course",
                    ),
                ),
                (
                    "creator",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="users.player"
                    ),
                ),
                (
                    "participants",
                    models.ManyToManyField(
                        related_name="participants",
                        through="tournaments.PlayerParticipation",
                        to="users.player",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="playerparticipation",
            name="tournament",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="tournaments.tournament"
            ),
        ),
        migrations.CreateModel(
            name="Invitation",
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
                            ("accepted", "Accepted"),
                            ("declined", "Declined"),
                        ],
                        default="pending",
                        max_length=20,
                    ),
                ),
                ("invited_players", models.ManyToManyField(to="users.player")),
                (
                    "tournament",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="tournaments.tournament",
                    ),
                ),
            ],
        ),
    ]
