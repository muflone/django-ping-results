# Generated by Django 3.0.6 on 2020-05-10 00:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ping_results', '0005_host_packet_size'),
    ]

    operations = [
        migrations.AddField(
            model_name='host',
            name='interface',
            field=models.CharField(blank=True, max_length=255, verbose_name='interface'),
        ),
    ]