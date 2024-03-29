# Generated by Django 4.2 on 2023-08-29 21:30

import django.core.validators
from django.db import migrations, models
import form.models


class Migration(migrations.Migration):

    dependencies = [
        ('form', '0015_coopform_president_position_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coopform',
            name='attach_bye_laws',
            field=models.FileField(blank=True, upload_to=form.models.CoopForm.get_upload_path, validators=[django.core.validators.FileExtensionValidator(['pdf', 'doc', 'docx', 'png', 'txt', 'jpg'])], verbose_name='Attach a copy of your Bye-Laws'),
        ),
        migrations.AlterField(
            model_name='coopform',
            name='society_logo',
            field=models.ImageField(blank=True, default='C:\\Users\\Admin\\Downloads\\EA\\djangoprojects\\coopformapp\\form/templates/static/img/default.png', upload_to=form.models.CoopForm.get_upload_path, verbose_name="Society's Logo"),
        ),
    ]
