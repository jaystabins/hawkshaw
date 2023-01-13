# Generated by Django 3.2.15 on 2023-01-13 16:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("projects", "0001_initial"),
        ("issues", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="issue",
            name="project",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="projects.project"
            ),
        ),
    ]
