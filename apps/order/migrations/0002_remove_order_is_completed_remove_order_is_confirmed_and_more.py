# Generated by Django 5.0.1 on 2024-01-12 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='is_completed',
        ),
        migrations.RemoveField(
            model_name='order',
            name='is_confirmed',
        ),
        migrations.AddField(
            model_name='order',
            name='delivery_time',
            field=models.CharField(default=1, max_length=50, verbose_name='Delivery time'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('waiting', 'Waiting'), ('confiemd', 'Confirmed'), ('completed', 'Completed'), ('cancelled', 'Cancelled')], default='waiting', max_length=100, verbose_name='Status'),
        ),
    ]