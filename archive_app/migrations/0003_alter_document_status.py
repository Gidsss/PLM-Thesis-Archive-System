# Generated by Django 4.2.16 on 2024-11-27 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('archive_app', '0002_alter_document_abstract_alter_document_advisor_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Approved', 'Approved')], default='Pending', max_length=10),
        ),
    ]
