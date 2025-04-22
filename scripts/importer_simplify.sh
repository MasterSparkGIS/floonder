HOST=$1
TOL=0.0001

PASSWORD=$2

PGPASSWORD=$PASSWORD psql -h $HOST -U rahman -d floonderdb -c "DELETE FROM spatial_data_services_administrationregion;"
PGPASSWORD=$PASSWORD psql -h $HOST -U rahman -d floonderdb -c "DELETE FROM spatial_data_services_rainfall;"
PGPASSWORD=$PASSWORD psql -h $HOST -U rahman -d floonderdb -c "DELETE FROM spatial_data_services_river;"
PGPASSWORD=$PASSWORD psql -h $HOST -U rahman -d floonderdb -c "DELETE FROM spatial_data_services_lake;"
PGPASSWORD=$PASSWORD psql -h $HOST -U rahman -d floonderdb -c "DELETE FROM spatial_data_services_slope;"
PGPASSWORD=$PASSWORD psql -h $HOST -U rahman -d floonderdb -c "DELETE FROM spatial_data_services_digitalelevationmodel;"
PGPASSWORD=$PASSWORD psql -h $HOST -U rahman -d floonderdb -c "DELETE FROM spatial_data_services_property;"
PGPASSWORD=$PASSWORD psql -h $HOST -U rahman -d floonderdb -c "DELETE FROM spatial_data_services_floodpoint;"

for SHP in \
  ../data/bandung-barat/ADMINISTRASIDESA_AR_25K.shp \
  ../data/kab-bandung/ADMINISTRASIDESA_AR_25K.shp \
  ../data/KOTABANDUNG/ADMINISTRASIDESA_AR_25K.shp
 do
  echo "Importing ADMINISTRASIDESA with simplification..."
  ogr2ogr -f "PostgreSQL" \
    PG:"dbname=floonderdb user=rahman password=$PASSWORD host=$HOST port=5432" \
    "$SHP" \
    -nln spatial_data_services_administrationregion \
    -append \
    -simplify $TOL
 done

for month in maret april mei
 do
  echo "Importing curah-hujan-$month.geojson with simplification..."
  ogr2ogr -f "PostgreSQL" \
    PG:"dbname=floonderdb user=rahman password=$PASSWORD host=$HOST port=5432" \
    ../data/processed/curah-hujan-$month.geojson \
    -nln spatial_data_services_rainfall \
    -append \
    -simplify $TOL
 done

for SHP in \
  ../data/kab-bandung/SUNGAI_LN_25K.shp \
  ../data/KOTABANDUNG/SUNGAI_LN_25K.shp \
  ../data/bandung-barat/SUNGAI_LN_25K.shp
 do
  echo "Importing SUNGAI_LN with simplification..."
  ogr2ogr -f "PostgreSQL" \
    PG:"dbname=floonderdb user=rahman password=$PASSWORD host=$HOST port=5432" \
    "$SHP" \
    -nln spatial_data_services_river \
    -append \
    -simplify $TOL
 done

for SHP in \
  ../data/KOTABANDUNG/DANAU_AR_25K.shp \
  ../data/kab-bandung/DANAU_AR_25K.shp \
  ../data/bandung-barat/DANAU_AR_25K.shp
 do
  echo "Importing DANAU_AR with simplification..."
  ogr2ogr -f "PostgreSQL" \
    PG:"dbname=floonderdb user=rahman password=$PASSWORD host=$HOST port=5432" \
    "$SHP" \
    -nln spatial_data_services_lake \
    -append \
    -simplify $TOL
 done

echo "Importing Property..."
ogr2ogr -f "PostgreSQL" \
  PG:"dbname=floonderdb user=rahman password=$PASSWORD host=$HOST port=5432" \
  ../data/survei-properti.geojson \
  -nln spatial_data_services_property \
  -append

echo "Importing Titik Banjir..."
for month in maret april mei juni juli agustus
 do
  ogr2ogr -f "PostgreSQL" \
    PG:"dbname=floonderdb user=rahman password=$PASSWORD host=$HOST port=5432" \
    "../data/titik_banjir_${month}_final.geojson" \
    -nln spatial_data_services_floodpoint \
    -append

  echo "Importing Titik Banjir $month..."
 done

raster2pgsql -s 4326 -I -C -M -F -t 256x256 -a ../data/reprojected-slope.tif spatial_data_services_slope | PGPASSWORD=$PASSWORD psql -h $HOST -U rahman -d floonderdb
raster2pgsql -s 4326 -I -C -M -F -t 256x256 -a ../data/dem-merged.tif spatial_data_services_digitalelevationmodel | PGPASSWORD=$PASSWORD psql -h $HOST -U rahman -d floonderdb