from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("vineapp", "0002_alter_customer_feedback_fields"),
    ]

    operations = [
        migrations.CreateModel(
            name="Product",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=140)),
                ("price", models.PositiveIntegerField()),
                ("size", models.CharField(max_length=20)),
                ("condition", models.CharField(max_length=30)),
                ("tag", models.CharField(blank=True, max_length=60)),
                ("image", models.URLField()),
                ("images", models.JSONField(blank=True, default=list)),
                ("description", models.TextField()),
                ("is_featured", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
