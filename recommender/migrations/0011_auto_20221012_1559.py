# Generated by Django 3.2.15 on 2022-10-12 19:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recommender', '0010_recentsearches'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recentsearches',
            name='results',
        ),
        migrations.AddField(
            model_name='recentsearches',
            name='result1',
            field=models.ManyToManyField(blank=True, null=True, related_name='result1', to='recommender.Musicdata'),
        ),
        migrations.AddField(
            model_name='recentsearches',
            name='result2',
            field=models.ManyToManyField(blank=True, null=True, related_name='result2', to='recommender.Musicdata'),
        ),
        migrations.AddField(
            model_name='recentsearches',
            name='result3',
            field=models.ManyToManyField(blank=True, null=True, related_name='result3', to='recommender.Musicdata'),
        ),
    ]
