# Generated by Django 5.0.3 on 2024-03-16 09:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='pdf_data_tb',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pdf_file', models.FileField(null=True, upload_to='pdf')),
                ('created_at', models.DateTimeField(default='', max_length=100)),
                ('updated_at', models.DateTimeField(default='', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='pdf_to_image_data_tb',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', max_length=100)),
                ('image', models.FileField(null=True, upload_to='pdf_images')),
                ('created_at', models.DateTimeField(default='', max_length=100)),
                ('updated_at', models.DateTimeField(default='', max_length=100)),
                ('pdf_id', models.ForeignKey(default='', null=True, on_delete=django.db.models.deletion.CASCADE, to='RealCostApp.pdf_data_tb')),
            ],
        ),
    ]
