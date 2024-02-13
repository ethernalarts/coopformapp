# Generated by Django 4.1.3 on 2023-01-05 10:19

from django.db import migrations, models
import form.models


class Migration(migrations.Migration):

    dependencies = [
        ('form', '0003_coopform_society_logo_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coopform',
            name='society_logo',
            field=models.ImageField(blank=True, default='images/default.png', upload_to=form.models.CoopForm.get_upload_path, verbose_name="Society's Logo"),
        ),
    ]
