# Generated by Django 5.0.3 on 2025-03-24 21:40

import django.contrib.gis.db.models.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('spatial_data_services', '0003_river_slope'),
    ]

    operations = [
        migrations.AlterField(
            model_name='administrationregion',
            name='geom',
            field=django.contrib.gis.db.models.fields.PolygonField(blank=True, null=True, srid=4326),
        ),
    ]
