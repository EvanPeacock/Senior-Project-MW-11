# Generated by Django 3.2.15 on 2022-11-09 22:37

from django.db import migrations, models
import recommender.models


class Migration(migrations.Migration):

    dependencies = [
        ('recommender', '0028_alter_artist_artist_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artist',
            name='artist_id',
            field=models.TextField(default=recommender.models.uniqueIDArtist, editable=False, primary_key=True, serialize=False),
        ),
    ]
