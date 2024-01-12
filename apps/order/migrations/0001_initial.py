# Generated by Django 5.0.1 on 2024-01-12 10:47

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('fastfood', '0002_alter_fastfood_restaurant'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('total_price', models.FloatField(default=0.0, verbose_name='Total price')),
                ('is_confirmed', models.BooleanField(default=False, verbose_name='Is confirmed')),
                ('is_completed', models.BooleanField(default=False, verbose_name='Is completed')),
                ('lon', models.FloatField(default=0.0, verbose_name='Longitute')),
                ('lat', models.FloatField(default=0.0, verbose_name='Latitude')),
                ('address', models.CharField(blank=True, max_length=255, null=True, verbose_name='Address')),
                ('created_by', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_%(model_name)ss', to=settings.AUTH_USER_MODEL)),
                ('restaurant', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to='fastfood.restaurant', verbose_name='Restaurant')),
                ('updated_by', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='updated_%(model_name)ss', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'Order',
                'verbose_name_plural': 'Orders',
                'db_table': 'order_order',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('count', models.IntegerField(default=0, verbose_name='Count')),
                ('price', models.FloatField(default=0.0, verbose_name='Price')),
                ('created_by', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_%(model_name)ss', to=settings.AUTH_USER_MODEL)),
                ('fastfood', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orderitems', to='fastfood.fastfood', verbose_name='Fast-food')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orderitems', to='order.order', verbose_name='Order')),
                ('updated_by', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='updated_%(model_name)ss', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Order Item',
                'verbose_name_plural': 'Order Items',
                'db_table': 'order_orderitem',
                'ordering': ['-created_at'],
            },
        ),
    ]