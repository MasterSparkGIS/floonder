ogr2ogr -f "PostgreSQL" \
  PG:"host=localhost port=5432 dbname=floonderdb user=rahman password=rahman" \
  administrasidesa_ar.geojson \
  -nln spatial_data_services_administrationregion \
  -nlt MULTIPOLYGON \
  -lco GEOMETRY_NAME=geometry \
  -skipfailures

ogr2ogr -f "PostgreSQL" \
  PG:"host=localhost port=5432 dbname=floonderdb user=rahman password=rahman" \
  output.geojson \
  -nln spatial_data_services_rainfall \
  -nlt POLYGON \
  -lco GEOMETRY_NAME=geometry \
  -skipfailures