from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("vineapp", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customer",
            name="full_name",
            field=models.CharField(max_length=120),
        ),
        migrations.AlterField(
            model_name="customer",
            name="message",
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name="customer",
            name="phonenumber",
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name="customer",
            name="product_name",
            field=models.CharField(blank=True, max_length=120),
        ),
        migrations.AlterField(
            model_name="customer",
            name="rating",
            field=models.CharField(blank=True, max_length=10),
        ),
    ]
