# Generated by Django 3.2.15 on 2022-11-16 21:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recommender', '0032_auto_20221116_2100'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profilepicture',
            old_name='profile_pic',
            new_name='profile_picture',
        ),
    ]
