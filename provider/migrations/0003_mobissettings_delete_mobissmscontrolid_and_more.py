# Generated by Django 5.0.4 on 2024-05-27 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('provider', '0002_mobissmscontrolid_sms'),
    ]

    operations = [
        migrations.CreateModel(
            name='MobisSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('login', models.CharField(max_length=120)),
                ('password', models.CharField(max_length=120)),
            ],
            options={
                'verbose_name': 'Mobis settings',
                'verbose_name_plural': 'Mobis settings',
            },
        ),
        migrations.DeleteModel(
            name='MobisSMSControlid',
        ),
        migrations.AlterModelOptions(
            name='sms',
            options={'verbose_name': 'SMS', 'verbose_name_plural': 'SMS'},
        ),
        migrations.AddField(
            model_name='sms',
            name='status',
            field=models.CharField(blank=True, choices=[('0', 'checking'), ('1', 'queued'), ('2', 'delivered'), ('3', 'failed')], max_length=20, null=True, verbose_name='Status'),
        ),
        migrations.AddField(
            model_name='sms',
            name='task_id',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
        migrations.AlterField(
            model_name='sms',
            name='msisdn',
            field=models.TextField(blank=True, max_length=120, null=True),
        ),
    ]
