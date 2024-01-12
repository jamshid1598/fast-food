# Generated by Django 5.0.1 on 2024-01-12 07:34

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fastfood', '0001_initial'),
        ('users', '0002_alter_users_user_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='users',
            name='user_type',
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user_type', models.CharField(choices=[('admin', 'Admin'), ('waiter', 'Waiter')], default='waiter', max_length=100, verbose_name='User type')),
                ('created_by', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_%(model_name)ss', to=settings.AUTH_USER_MODEL)),
                ('restaurant', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='employees', to='fastfood.restaurant', verbose_name='restaurant')),
                ('updated_by', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='updated_%(model_name)ss', to=settings.AUTH_USER_MODEL)),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='employee', to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'verbose_name': 'Employee',
                'verbose_name_plural': 'Employees',
                'db_table': 'users_employees',
            },
        ),
    ]
