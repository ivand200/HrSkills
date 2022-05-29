# Generated by Django 4.0.4 on 2022-05-25 07:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0004_remove_tag_clients_client_tag'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='tag',
            field=models.ManyToManyField(null=True, to='hr.tag'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='title',
            field=models.CharField(max_length=20, unique=True),
        ),
    ]