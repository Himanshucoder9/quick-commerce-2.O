# Generated by Django 4.2 on 2024-08-06 11:41

import Master.myvalidator
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Auth', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Warehouse', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='cart', to='Auth.customer', verbose_name='customer')),
            ],
            options={
                'verbose_name': 'Cart',
                'verbose_name_plural': 'Carts',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_number', models.CharField(max_length=15, unique=True, verbose_name='Order Number')),
                ('total_amount', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='total amount')),
                ('order_status', models.CharField(choices=[('Pending', 'Pending'), ('Processing', 'Processing'), ('Completed', 'Completed'), ('Canceled', 'Canceled')], default='Pending', max_length=50, verbose_name='order status')),
                ('payment_method', models.CharField(choices=[('Online', 'Online'), ('COD', 'Cash on Delivery')], max_length=20, verbose_name='payment method')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created date')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='Auth.customer', verbose_name='customer')),
            ],
            options={
                'verbose_name': 'Order',
                'verbose_name_plural': 'Orders',
            },
        ),
        migrations.CreateModel(
            name='ShippingAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created date')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated date')),
                ('customer_name', models.CharField(max_length=200, verbose_name='customer name')),
                ('customer_phone', models.CharField(help_text='Alphabets and special characters are not allowed.', max_length=13, validators=[Master.myvalidator.mobile_validator], verbose_name='customer mobile number')),
                ('address_type', models.CharField(choices=[('Home', 'Home'), ('Work', 'Work'), ('Hotel', 'Hotel'), ('Other', 'Other')], default='home', max_length=10, verbose_name='address type')),
                ('building_name', models.CharField(max_length=255, verbose_name='Flat/House No./Building Name')),
                ('floor', models.CharField(blank=True, max_length=20, null=True, verbose_name='Floor')),
                ('landmark', models.CharField(blank=True, max_length=255, null=True, verbose_name='Nearby Landmark')),
                ('latitude', models.DecimalField(decimal_places=6, max_digits=9, verbose_name='Latitude')),
                ('longitude', models.DecimalField(decimal_places=6, max_digits=9, verbose_name='Longitude')),
                ('full_address', models.TextField(verbose_name='full address')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Auth.customer', verbose_name='customer')),
            ],
            options={
                'verbose_name': 'Shipping Address',
                'verbose_name_plural': 'Shipping Addresses',
            },
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_method', models.CharField(choices=[('Online', 'Online'), ('COD', 'Cash on Delivery')], max_length=20, verbose_name='payment method')),
                ('razorpay_order_id', models.CharField(blank=True, max_length=200, null=True, verbose_name='Razorpay Order ID')),
                ('razorpay_payment_id', models.CharField(blank=True, max_length=200, null=True, verbose_name='Razorpay Payment ID')),
                ('razorpay_payment_status', models.CharField(blank=True, max_length=50, null=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='amount')),
                ('payment_status', models.CharField(choices=[('Pending', 'Pending'), ('Completed', 'Completed'), ('Canceled', 'Canceled')], max_length=50, verbose_name='payment status')),
                ('payment_date', models.DateTimeField(auto_now_add=True, verbose_name='payment date')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments', to=settings.AUTH_USER_MODEL, verbose_name='customer')),
                ('order', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='Customer.order', verbose_name='order')),
            ],
            options={
                'verbose_name': 'Payment',
                'verbose_name_plural': 'Payments',
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1, verbose_name='quantity')),
                ('item_price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='item price')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created date')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='Customer.order', verbose_name='order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Warehouse.product', verbose_name='product')),
                ('warehouse', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='Auth.warehouse', verbose_name='warehouse')),
            ],
            options={
                'verbose_name': 'Order Item',
                'verbose_name_plural': 'Order Items',
            },
        ),
        migrations.AddField(
            model_name='order',
            name='shipping_address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Customer.shippingaddress', verbose_name='shipping address'),
        ),
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created date')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated date')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorites', to='Auth.customer', verbose_name='customer')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorites', to='Warehouse.product', verbose_name='product')),
            ],
            options={
                'verbose_name': 'Favorite',
                'verbose_name_plural': 'Favorites',
            },
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1, verbose_name='quantity')),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cart_items', to='Customer.cart', verbose_name='cart')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Warehouse.product', verbose_name='product')),
            ],
            options={
                'verbose_name': 'Cart Item',
                'verbose_name_plural': 'Cart Items',
            },
        ),
    ]
