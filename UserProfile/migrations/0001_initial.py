# Generated by Django 4.2.2 on 2023-06-26 08:43

import UserProfile.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gender', models.CharField(choices=[('male', 'Male'), ('female', 'Female'), ('others', 'Others')], default='male', max_length=20)),
                ('dob', models.DateField(blank=True, default=None, null=True)),
                ('phone', models.CharField(blank=True, max_length=20, null=True)),
                ('works_at', models.CharField(blank=True, max_length=200, null=True)),
                ('lives_in', models.CharField(blank=True, max_length=200, null=True)),
                ('studies_at', models.CharField(blank=True, max_length=200, null=True)),
                ('profile_image', models.ImageField(blank=True, upload_to=UserProfile.models.nameFile)),
                ('roles', models.CharField(choices=[('student', 'Student'), ('teacher', 'Teacher')], default='student', max_length=10)),
                ('owner', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile_data', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
