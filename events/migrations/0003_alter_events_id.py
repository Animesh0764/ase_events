# Generated by Django 5.1.4 on 2024-12-14 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_email_attendee'),
    ]

    operations = [
        migrations.AlterField(
            model_name='events',
            name='id',
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
    ]