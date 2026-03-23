# Generated migration to add email and created_at fields to customer model

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vineapp', '0006_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='email',
            field=models.EmailField(default='noemail@example.com', max_length=254),
        ),
        migrations.AddField(
            model_name='customer',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
