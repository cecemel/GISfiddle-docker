#What
Loads data into PostGIS backend according to the 'pgsnapshot_schema' </br>
Depends on [Osmosis](http://wiki.openstreetmap.org/wiki/Osmosis/) and custom python script to load the data. <br>
You can import data incrementally, i.e. upload different (even overlapping) regions.

#How
see previous README for the commands.
There is sample data in data folder. If you kept all defaults, just replace data.osm.bz2 with the region of your choice. 
I get my data from [geofabrik](http://download.geofabrik.de/europe.html). </br>
Check the python scipt enviroment variables for non-default stuff, like (told you it wasn't safe) passwords, etc
