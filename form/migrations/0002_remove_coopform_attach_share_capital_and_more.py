# Generated by Django 4.1.3 on 2022-12-30 09:34

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('form', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='coopform',
            name='attach_share_capital',
        ),
        migrations.AddField(
            model_name='coopform',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='coopform',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='coopform',
            name='attach_bye_laws',
            field=models.FileField(blank=True, upload_to='documents', verbose_name='Attach a copy of your Bye-Laws'),
        ),
        migrations.AlterField(
            model_name='coopform',
            name='first_contact_email',
            field=models.EmailField(blank=True, max_length=254, verbose_name="1st Contact's Email"),
        ),
        migrations.AlterField(
            model_name='coopform',
            name='first_purpose',
            field=models.CharField(max_length=300, verbose_name='First Purpose'),
        ),
        migrations.AlterField(
            model_name='coopform',
            name='have_bye_laws',
            field=models.CharField(default='No', max_length=128),
        ),
        migrations.AlterField(
            model_name='coopform',
            name='id',
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='coopform',
            name='nature_registration',
            field=models.CharField(max_length=100, verbose_name='Nature of Registration'),
        ),
        migrations.AlterField(
            model_name='coopform',
            name='second_contact_email',
            field=models.EmailField(blank=True, max_length=254, verbose_name="2nd Contact's Email"),
        ),
        migrations.AlterField(
            model_name='coopform',
            name='second_purpose',
            field=models.CharField(max_length=300, verbose_name='Second Purpose'),
        ),
        migrations.AlterField(
            model_name='coopform',
            name='third_contact_email',
            field=models.EmailField(blank=True, max_length=254, verbose_name="3rd Contact's Email"),
        ),
        migrations.AlterField(
            model_name='coopform',
            name='third_purpose',
            field=models.CharField(max_length=300, verbose_name='Third Purpose'),
        ),
        migrations.CreateModel(
            name='shareCapitalFiles',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('attach_share_capital', models.FileField(blank=True, upload_to='documents/share_capital_files', verbose_name='Attach Share Capital')),
                ('coopform', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='files', to='form.coopform')),
            ],
            options={
                'db_table': 'form_sharecapitalfiles',
            },
        ),
    ]
