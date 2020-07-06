# Generated by Django 3.0.8 on 2020-07-06 15:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('responses', '0003_auto_20200706_0047'),
    ]

    operations = [
        migrations.AlterField(
            model_name='responses',
            name='status',
            field=models.CharField(choices=[('Submitted', 'Submitted'), ('Written', 'Written'), ('Uploaded', 'Uploaded')], default='Submitted', max_length=20),
        ),
    ]
