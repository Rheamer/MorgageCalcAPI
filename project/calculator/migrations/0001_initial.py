# Generated by Django 3.1.6 on 2022-05-06 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Offer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bank_name', models.CharField(max_length=100)),
                ('term_min', models.IntegerField()),
                ('term_max', models.IntegerField()),
                ('rate_min', models.FloatField()),
                ('rate_max', models.FloatField()),
                ('payment_min', models.FloatField()),
                ('payment_max', models.FloatField()),
            ],
        ),
    ]