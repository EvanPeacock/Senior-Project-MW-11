# Generated by Django 3.2.15 on 2022-10-03 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recommender', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_fname', models.CharField(max_length=50)),
                ('user_lname', models.CharField(max_length=50)),
                ('user_email', models.EmailField(max_length=254)),
                ('user_password', models.CharField(max_length=50)),
            ],
        ),
    ]
