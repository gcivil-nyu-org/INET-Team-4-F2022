# Generated by Django 2.2 on 2022-11-14 03:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0014_merge_20221111_0455'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['-title']},
        ),
    ]