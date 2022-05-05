# Generated by Django 3.2.10 on 2022-01-14 21:02

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic', models.CharField(max_length=20)),
                ('question', models.TextField()),
                ('answers', models.TextField()),
                ('correct_answers', models.TextField()),
            ],
        ),
    ]
