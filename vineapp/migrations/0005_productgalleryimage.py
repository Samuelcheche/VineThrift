from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("vineapp", "0004_alter_product_image"),
    ]

    operations = [
        migrations.CreateModel(
            name="ProductGalleryImage",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("image", models.ImageField(upload_to="products/gallery/")),
                ("sort_order", models.PositiveIntegerField(default=0)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "product",
                    models.ForeignKey(on_delete=models.deletion.CASCADE, related_name="gallery_images", to="vineapp.product"),
                ),
            ],
            options={"ordering": ["sort_order", "id"]},
        ),
    ]
