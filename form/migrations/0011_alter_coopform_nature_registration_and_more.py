# Generated by Django 4.2 on 2023-07-30 18:09

from django.db import migrations, models
import django.db.models.deletion
import form.models


class Migration(migrations.Migration):

    dependencies = [
        ('form', '0010_remove_coopform_is_cooperative_remove_coopform_user_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coopform',
            name='nature_registration',
            field=models.CharField(choices=[('Limited Liability', 'Limited Liability'), ('Without Limited Liability', 'Without Limited Liability')], max_length=100, verbose_name='Nature of Registration'),
        ),
        migrations.AlterField(
            model_name='coopform',
            name='society_logo',
            field=models.ImageField(blank=True, default='C:\\Users\\Admin\\Downloads\\EA\\djangoprojects\\coopformapp\\form/templates/static/img/default.png', upload_to=form.models.CoopForm.get_upload_path, verbose_name="Society's Logo"),
        ),
        migrations.AlterField(
            model_name='sharecapitalfiles',
            name='coopform',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='share_capital_files', to='form.coopform'),
        ),
    ]
