# Generated by Django 3.1.4 on 2021-01-02 10:30

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Facultad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255)),
                ('alias', models.CharField(max_length=3)),
                ('creado', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'db_table': 'facultad',
            },
        ),
        migrations.CreateModel(
            name='TipoPersonal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=256)),
                ('alias', models.CharField(max_length=3)),
                ('creado', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'db_table': 'tipo_personal',
            },
        ),
        migrations.CreateModel(
            name='Personal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255)),
                ('apellidos', models.CharField(max_length=255)),
                ('codigo', models.CharField(max_length=255, null=True)),
                ('correo', models.EmailField(max_length=255)),
                ('encoded_image', models.TextField()),
                ('creado', models.DateTimeField(default=django.utils.timezone.now)),
                ('facultad', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='facultad', to='personal.facultad')),
                ('tipo_personal', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='tipo_personal', to='personal.tipopersonal')),
            ],
            options={
                'db_table': 'personal',
            },
        ),
    ]
