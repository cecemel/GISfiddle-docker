# -*- coding: utf-8 -*-
"""
Created on Sun Mar 20 14:54:30 2016

@author: fruizdearcaute
"""
import os
import subprocess
import tempfile
import logging
import shutil

def init_db(config, stop_on_error=True):
     #DO NOT CHANGE THE ORDER OF THE SCHEMAS OSMOSIS LIKES ORDER)
    scripts = [os.path.join(config['osmosis_dir'],'script/pgsnapshot_schema_0.6.sql')]
    scripts.append(os.path.join(config['osmosis_dir'],'script/pgsnapshot_schema_0.6_bbox.sql'))
    scripts.append(os.path.join(config['osmosis_dir'],'script/pgsnapshot_schema_0.6_linestring.sql'))
    scripts.append(os.path.join(config['osmosis_dir'],'script/pgsnapshot_schema_0.6_action.sql'))

    command = " psql -U {} -d {} -h {}".format(config['user'], config['database'],
                                                          config['host'])
    if stop_on_error:
             command += ' -v ON_ERROR_STOP=1'
    #executes the init scripts
    [subprocess.check_output(command + ' -f ' + script, shell=True) for script in scripts]

def load_data_pg_simple_schema_data(config, osm_file, temp_directory, java_Xmx=2, stop_on_error=True):
    """
    procedure to import osm file to populate db

    Note: original commands
    -----------------

    cat /tmp/belgium-latest.osm | /tmp/osmosis/bin/osmosis
          --fast-read-xml file=- --sort --log-progress interval=30
          --write-pgsql-dump directory=/tmp/osmosis_temp enableBboxBuilder=yes
          enableLinestringBuilder=yes nodeLocationStoreType=CompactTempFile

    cd /tmp/osmosis_temp;
    psql -U postgres -d xapi -f /tmp/osmosis/script/pgsnapshot_load_0.6.sql;
    """
    curr_dir = os.getcwd()

    #import data script
    import_script = os.path.join(curr_dir, config['osmosis_dir'],'script/pgsnapshot_load_0.6.sql')
    config['logger'].info('Working in: {}'.format(curr_dir))
    java_tmp = tempfile.mkdtemp(dir=temp_directory)
    temp_dir = tempfile.mkdtemp(dir=temp_directory)

    try:
        #prepare file (note play with java Xmx set @ 16G)
        command  = 'export JAVACMD_OPTIONS="-Xmx{}G -Djava.io.tmpdir={}";'.format(java_Xmx, java_tmp)
        os.system(command)

        #DO NOT CHANGE THE POSITION OF LINESTRINGBUILDER, IT MIGHT FUCK UP EVERYTHING
        #(IF YOU SEE POLYGON IN LINESTRING FIELD, SOMETHING IS POSSIBLY WRONG, OSMOSIS LIKES ORDER)
        #POSSIBLY ONLY AFFECTING 0.43 (latest version)
        command += "bzcat {} |".format(osm_file)
        command += " {} --fast-read-xml file=- --sort --log-progress interval=30".format(config['bin_path'])
        command +=" --write-pgsql-dump directory={}".format(temp_dir)
        command +=" enableBboxBuilder=yes enableLinestringBuilder=yes nodeLocationStoreType=CompactTempFile"

        config['logger'].info('Executing: {}'.format(command))

        subprocess.check_output(command, shell=True)

        command = "export PGPASSWORD={};".format(config['password'])
        command += " psql -U {} -d {} -h {} -f {}".format(config['user'], config['database'],
                                                  config['host'], import_script)

        if stop_on_error:
             command += ' -v ON_ERROR_STOP=1'

        os.chdir(temp_dir) #easier if we change dir
        config['logger'].info('Executing: {}'.format(command))

        subprocess.check_output(command, shell = True)

        config['logger'].info('Finished import')

    except Exception as e:
        raise e
    finally:
        config['logger'].info('Moving back to {}'.format(curr_dir))
        os.chdir(curr_dir)

if __name__ == "__main__":
    ####################################################################################################################
    # INIT DEFAULT STUFF (leave as is, unless you're doing non-default stuff)
    ####################################################################################################################
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')
    logger = logging.getLogger(__name__)
    config = {'host': '', 'database': '', 'user': '', 'password' : '', 'logger': logger}
    config['osmosis_dir'] = 'osmosis_latest'
    config['bin_path'] = os.path.join(config['osmosis_dir'], 'bin/osmosis')
    osm_file = 'data.osm.bz2'
    temp_dir = tempfile.mkdtemp()
    java_Xmx = 2
    stop_on_error = True
    ####################################################################################################################
    # INIT YOUR CONFIG
    ####################################################################################################################
    config['host'] = os.environ.get('DBHOST','postgis_db')
    config['database'] = os.environ.get('DBNAME','gis_fiddle')
    config['user'] = os.environ.get('DBUSER','postgres')
    config['password'] = os.environ.get('DBPASS','')

    config['logger'].info('Using {}'.format(config))

    java_Xmx = int(os.environ.get('Xmx','2'))

    ####################################################################################################################
    # IMPORT!
    ####################################################################################################################
    init_db(config)
    load_data_pg_simple_schema_data(config, osm_file, temp_dir, java_Xmx, stop_on_error)

    #cleanup (only when no errors)
    shutil.rmtree(temp_dir)

    config['logger'].info('!SUCCESS!')
