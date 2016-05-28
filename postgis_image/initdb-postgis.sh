#!/bin/sh

set -e

# Perform all actions as $POSTGRES_USER
export PGUSER="$POSTGRES_USER"

# Create the 'template_postgis' template db
psql --dbname="$POSTGRES_DB" <<- 'EOSQL'
CREATE DATABASE template_postgis;
UPDATE pg_database SET datistemplate = TRUE WHERE datname = 'template_postgis';
EOSQL

# Load PostGIS into both template_database and $POSTGRES_DB
cd "/usr/share/postgresql/$PG_MAJOR/contrib/postgis-$POSTGIS_MAJOR"
for DB in template_postgis "$POSTGRES_DB"; do
	if awk "BEGIN { exit $PG_MAJOR >= 9.1 ? 0 : 1 }"; then
		echo "Loading PostGIS into $DB via CREATE EXTENSION"
		psql --dbname="$DB" <<-'EOSQL'
			CREATE EXTENSION postgis;
			CREATE EXTENSION postgis_topology;
			CREATE EXTENSION fuzzystrmatch;
			CREATE EXTENSION postgis_tiger_geocoder;
		EOSQL
	else
		echo "Loading PostGIS into $DB via files"
		files='
			postgis
			postgis_comments
			topology
			topology_comments
			rtpostgis
			raster_comments
		'
		for file in $files; do
			psql --dbname="$DB" < "${file}.sql"
		done
	fi
done
#http://stackoverflow.com/questions/760210/how-do-you-create-a-read-only-user-in-postgresql
psql <<- EOSQL
    ALTER DATABASE "template_postgis" RENAME TO "gis_fiddle";
    GRANT ALL PRIVILEGES ON DATABASE gis_fiddle TO postgres;
    CREATE USER gis_fiddle_user;
    GRANT SELECT ON ALL TABLES IN SCHEMA public TO gis_fiddle_user;
    GRANT SELECT ON ALL SEQUENCES IN SCHEMA public TO gis_fiddle_user;
    ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO gis_fiddle_user;
    \connect gis_fiddle;
    CREATE EXTENSION hstore;
EOSQL
#move some config files
cp $PGCONFIG/postgresql.conf $PGDATA/
