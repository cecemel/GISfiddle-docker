# GISfiddle-docker

docker-files to help setup [GISfiddle](https://github.com/cecemel/GISfiddle) environment

##Run
By default no security measures are set up.
So if you want a public facing app, check the relevant image folders and docker files.

Assuming you didn't change any settings, the following should work
### Start environment
`docker-compose up`

###Import data
Note: required only the first time. Check readme import_postgis_data_image if you want to add more/different data.

`cd  import_postgis_data_image;`

`docker build -t data-importer .;`

`docker run -it --link gisfiddledocker_gis-fiddle-db_1:postgis_db data-importer;`
