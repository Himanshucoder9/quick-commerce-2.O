# Generated by Django 4.2 on 2024-08-06 11:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Auth', '0001_initial'),
        ('Customer', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeliveryAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created date')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated date')),
                ('status', models.CharField(choices=[('PROCESSING', 'Processing'), ('PICKED_UP', 'Picked Up'), ('IN_TRANSIT', 'In Transit'), ('DELIVERED', 'Delivered'), ('CANCELLED', 'Cancelled')], default='pending', max_length=20, verbose_name='status')),
                ('delivery_radius', models.FloatField(default=500, verbose_name='delivery radius')),
                ('otp', models.CharField(blank=True, max_length=6, null=True, verbose_name='OTP')),
                ('otp_created_at', models.DateTimeField(blank=True, null=True, verbose_name='OTP created')),
                ('driver', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Auth.driver', verbose_name='driver')),
                ('orders', models.ManyToManyField(related_name='deliveries', to='Customer.order', verbose_name='order')),
            ],
            options={
                'verbose_name': 'Delivery',
                'verbose_name_plural': 'Deliveries',
            },
        ),
    ]
