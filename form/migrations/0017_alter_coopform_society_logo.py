# Generated by Django 4.2 on 2023-08-29 21:31

from django.db import migrations, models
import form.models


class Migration(migrations.Migration):

    dependencies = [
        ('form', '0016_alter_coopform_attach_bye_laws_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coopform',
            name='society_logo',
            field=models.ImageField(blank=True, default='C:\\Users\\Admin\\Downloads\\EA\\djangoprojects\\coopformapp\\form/templates/static/img/default.png', upload_to=form.models.CoopForm.get_upload_path, verbose_name="Society's Logo"),
        ),
    ]