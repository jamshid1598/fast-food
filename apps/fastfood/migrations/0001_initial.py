# Generated by Django 5.0.1 on 2024-01-12 07:13

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('description', models.TextField(verbose_name='Description')),
                ('lon', models.FloatField(default=0.0, verbose_name='Longitude')),
                ('lat', models.FloatField(default=0.0, verbose_name='Latitude')),
                ('address', models.CharField(blank=True, max_length=255, null=True, verbose_name='Address')),
                ('contact', models.CharField(blank=True, max_length=255, null=True, verbose_name='Contact')),
                ('created_by', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_%(model_name)ss', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='updated_%(model_name)ss', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Fast-Food Restaurant',
                'verbose_name_plural': 'Fast-Food Restaurant',
                'db_table': ' fast_food_restaurant',
            },
        ),
        migrations.CreateModel(
            name='FastFood',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='fasd-food-images/', verbose_name='Image')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('description', models.TextField(verbose_name='Description')),
                ('price', models.FloatField(default=0.0, verbose_name='Price')),
                ('created_by', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_%(model_name)ss', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='updated_%(model_name)ss', to=settings.AUTH_USER_MODEL)),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fastfoods', to='fastfood.restaurant', verbose_name='Restaurant')),
            ],
            options={
                'verbose_name': 'Fast Food',
                'verbose_name_plural': 'Fast Food',
                'db_table': 'fast_food',
            },
        ),
    ]
