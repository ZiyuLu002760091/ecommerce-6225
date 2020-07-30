# Generated by Django 3.0.7 on 2020-07-30 18:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0001_initial'),
        ('payment_gateway', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='checkout',
            name='payment_method',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='payment_gateway.PaymentMethod', verbose_name='payment method'),
        ),
        migrations.AddField(
            model_name='checkout',
            name='status',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='status', to='core.Status'),
        ),
        migrations.AddField(
            model_name='book',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='categories_books', to='core.Category'),
        ),
        migrations.AddField(
            model_name='address',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_client_address', to='core.Customer'),
        ),
    ]
