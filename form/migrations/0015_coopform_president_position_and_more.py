# Generated by Django 4.2 on 2023-08-26 16:13

from django.db import migrations, models
import form.models


class Migration(migrations.Migration):

    dependencies = [
        ('form', '0014_alter_coopform_society_logo'),
    ]

    operations = [
        migrations.AddField(
            model_name='coopform',
            name='president_position',
            field=models.CharField(blank=True, default='President', max_length=100, verbose_name="President's Position"),
        ),
        migrations.AddField(
            model_name='coopform',
            name='secretary_position',
            field=models.CharField(blank=True, default='Secretary', max_length=100, verbose_name="Secretary's Position"),
        ),
        migrations.AddField(
            model_name='coopform',
            name='treasurer_position',
            field=models.CharField(blank=True, default='Treasurer', max_length=100, verbose_name="Treasurer's Position"),
        ),
        migrations.AlterField(
            model_name='coopform',
            name='have_bye_laws',
            field=models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], default='No', max_length=128),
        ),
        migrations.AlterField(
            model_name='coopform',
            name='society_logo',
            field=models.ImageField(blank=True, default='C:\\Users\\Admin\\Downloads\\EA\\djangoprojects\\coopformapp\\form/templates/static/img/default.png', upload_to=form.models.CoopForm.get_upload_path, verbose_name="Society's Logo"),
        ),
    ]
