# Generated by Django 5.1.4 on 2024-12-11 08:32

import api.models
import datetime
import django.contrib.auth.models
import django.db.models.deletion
import django.utils.timezone
import phonenumber_field.modelfields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Meal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('amount', models.IntegerField()),
                ('unit', models.CharField(choices=[('piece', 'Adet'), ('gram', 'Gram'), ('liter', 'Litre')], default='piece', max_length=10)),
                ('protein', models.IntegerField(default=0, help_text='Protein miktarı (gram)')),
                ('carbs', models.IntegerField(default=0, help_text='Karbonhidrat miktarı (gram)')),
                ('oil', models.IntegerField(default=0, help_text='Yağ miktarı (gram)')),
                ('calories', models.IntegerField(default=0, help_text='Kalori miktarı (kcal)')),
            ],
            options={
                'verbose_name': 'Yemek',
                'verbose_name_plural': 'Yemekler',
            },
        ),
        migrations.CreateModel(
            name='Movement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('video', models.URLField(help_text='YouTube video linki')),
                ('sets', models.IntegerField(default=3, help_text='Set sayısı', validators=[api.models.MinValueValidator(1)])),
                ('reps', models.IntegerField(default=12, help_text='Tekrar sayısı', validators=[api.models.MinValueValidator(1)])),
            ],
            options={
                'verbose_name': 'Hareket',
                'verbose_name_plural': 'Hareketler',
            },
        ),
        migrations.CreateModel(
            name='Diet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('meals', models.ManyToManyField(help_text='Birden fazla seçmek için CTRL tuşuna basılı tutun.', to='api.meal')),
            ],
            options={
                'verbose_name': 'Diyet',
                'verbose_name_plural': 'Diyetler',
            },
        ),
        migrations.CreateModel(
            name='Program',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('movements', models.ManyToManyField(help_text='Birden fazla seçmek için CTRL tuşuna basılı tutun.', to='api.movement')),
            ],
            options={
                'verbose_name': 'Program',
                'verbose_name_plural': 'Programlar',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(default='+900000000000', help_text='Kullanıcı telefon numarası', max_length=128, region=None, unique=True)),
                ('height', models.DecimalField(blank=True, decimal_places=2, help_text='Boy (cm)', max_digits=5, null=True)),
                ('weight', models.DecimalField(blank=True, decimal_places=2, help_text='Kilo (kg)', max_digits=5, null=True)),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('blood_type', models.CharField(blank=True, choices=[('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'), ('AB+', 'AB-'), ('AB-', 'AB-'), ('0+', '0+'), ('0-', '0-')], max_length=3, null=True)),
                ('membership_start', models.DateField(default=datetime.date.today, help_text='Üyelik başlangıç tarihi')),
                ('membership_end', models.DateField(help_text='Üyelik bitiş tarihi', null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
                ('diet', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.diet', verbose_name='Diyet')),
                ('program', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.program', verbose_name='Program')),
            ],
            options={
                'verbose_name': 'Kullanıcı',
                'verbose_name_plural': 'Kullanıcılar',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
