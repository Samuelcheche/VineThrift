from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("vineapp", "0003_product"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="image",
            field=models.ImageField(upload_to="products/"),
        ),
    ]
