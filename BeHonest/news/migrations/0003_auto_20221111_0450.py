# Generated by Django 2.2 on 2022-11-11 04:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("news", "0002_newscomment"),
    ]

    operations = [
        migrations.AlterField(
            model_name="news",
            name="id",
            field=models.AutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
        migrations.AlterField(
            model_name="newscomment",
            name="id",
            field=models.AutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
        migrations.AlterField(
            model_name="newscomment",
            name="post",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="newscomment",
                to="news.News",
            ),
        ),
    ]
