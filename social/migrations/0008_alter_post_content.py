# Generated by Django 4.0.1 on 2022-01-09 23:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0007_alter_post_images'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='content',
            field=models.TextField(),
        ),
    ]
