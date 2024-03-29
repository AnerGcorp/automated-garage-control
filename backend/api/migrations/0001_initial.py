# Generated by Django 5.0.1 on 2024-01-14 02:53

import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CarModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rfid', models.CharField(max_length=255, null=True)),
                ('model_car', models.CharField(max_length=255)),
                ('license_number', models.CharField(max_length=255)),
                ('corr_principal', models.TextField(blank=True)),
                ('belongs_building', models.TextField(blank=True)),
                ('car_photo', models.ImageField(blank=True, null=True, upload_to='cars/')),
                ('note', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Officer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('military_title', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('surname', models.CharField(max_length=255)),
                ('last_name', models.CharField(blank=True, max_length=255)),
                ('position', models.TextField(blank=True)),
                ('photo', models.ImageField(blank=True, null=True, upload_to='officier/')),
                ('note', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Soldier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('military_title', models.CharField(max_length=255)),
                ('photo', models.ImageField(blank=True, null=True, upload_to='soldier/')),
                ('name', models.CharField(max_length=255)),
                ('surname', models.CharField(max_length=255)),
                ('last_name', models.CharField(blank=True, max_length=255)),
                ('birthday', models.CharField(blank=True, max_length=255)),
                ('birth_place', models.TextField(blank=True)),
                ('nationality', models.CharField(blank=True, max_length=50)),
                ('knowledge', models.TextField(blank=True)),
                ('marriage_status', models.CharField(blank=True, max_length=50)),
                ('invited_hw', models.TextField(blank=True)),
                ('being_abroad', models.TextField(blank=True)),
                ('last_job', models.TextField(blank=True)),
                ('last_illness', models.TextField(blank=True)),
                ('harby_kasam_date', models.CharField(blank=True, max_length=255)),
                ('being_in_prison', models.TextField(blank=True)),
                ('home_address', models.TextField(blank=True)),
                ('specific_notes', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='CarMovement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(default=django.utils.timezone.now)),
                ('movement', models.CharField(choices=[('Girdi', 'Girdi'), ('Çykdy', 'Chykdy')], default='Girdi', max_length=7)),
                ('screenshot', models.ImageField(blank=True, null=True, upload_to='movement/')),
                ('note', models.TextField(blank=True)),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.carmodel')),
            ],
        ),
        migrations.AddField(
            model_name='carmodel',
            name='patron',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='api.officer'),
        ),
        migrations.CreateModel(
            name='Duty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('place', models.TextField(blank=True)),
                ('position', models.TextField(blank=True)),
                ('date', models.DateField()),
                ('note', models.TextField(blank=True)),
                ('on_duty', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='api.soldier')),
            ],
        ),
        migrations.CreateModel(
            name='CloseRelative',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('relative_degree', models.CharField(max_length=50)),
                ('birth_year', models.PositiveIntegerField(default=1900, validators=[django.core.validators.MaxValueValidator(2024), django.core.validators.MinValueValidator(1900)])),
                ('aaa_field', models.TextField()),
                ('work_place_and_position', models.TextField(max_length=5000)),
                ('belongs_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='soldier_relative', to='api.soldier')),
            ],
        ),
        migrations.AddField(
            model_name='carmodel',
            name='driver',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='api.soldier'),
        ),
        migrations.CreateModel(
            name='BeenMilitaryBase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('military_base', models.CharField(max_length=50)),
                ('military_acc_pos', models.CharField(blank=True, max_length=100)),
                ('military_base_enter_date', models.CharField(blank=True, max_length=255)),
                ('military_base_exit_date', models.CharField(blank=True, max_length=255)),
                ('belongs_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='soldier_base', to='api.soldier')),
            ],
        ),
    ]
