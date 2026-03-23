from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("vineapp", "0005_productgalleryimage"),
    ]

    operations = [
        migrations.CreateModel(
            name="Order",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("customer_name", models.CharField(max_length=140)),
                ("customer_email", models.EmailField(max_length=254)),
                ("phone_number", models.CharField(max_length=20)),
                ("delivery_location", models.CharField(max_length=200)),
                ("notes", models.TextField(blank=True)),
                ("product_name", models.CharField(max_length=140)),
                ("product_price", models.PositiveIntegerField()),
                ("delivery_fee", models.PositiveIntegerField(default=300)),
                ("total_amount", models.PositiveIntegerField()),
                ("payment_method", models.CharField(default="mpesa", max_length=40)),
                ("payment_status", models.CharField(default="stk_sent", max_length=30)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "product",
                    models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="orders", to="vineapp.product"),
                ),
            ],
        ),
    ]
