# Generated by Django 3.0.6 on 2020-05-09 00:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ping_results', '0001_host'),
    ]

    operations = [
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(verbose_name='timestamp')),
                ('status', models.BooleanField(verbose_name='status')),
                ('elapsed', models.FloatField(verbose_name='elapsed time')),
                ('host', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='ping_results.Host', verbose_name='host')),
            ],
            options={
                'verbose_name': 'Result',
                'verbose_name_plural': 'Results',
                'db_table': 'ping_results_results',
                'ordering': ['-timestamp', 'host'],
                'unique_together': {('host', 'timestamp')},
            },
        ),
    ]