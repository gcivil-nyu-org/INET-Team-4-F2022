# Generated by Django 2.2 on 2022-11-07 22:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("post", "0012_merge_0010_auto_20221103_0034_0011_auto_20221104_0145"),
    ]

    operations = [
        migrations.AlterField(
            model_name="comment",
            name="id",
            field=models.AutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
        migrations.AlterField(
            model_name="post",
            name="id",
            field=models.AutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
    ]
