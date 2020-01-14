kakadatabase-back
=================

[![Build Status](https://api.travis-ci.com/electricmagnetic/kakadatabase-back.svg?branch=master)](https://travis-ci.com/electricmagnetic/kakadatabase-back)
[![codecov](https://codecov.io/gh/electricmagnetic/kakadatabase-back/branch/master/graph/badge.svg)](https://codecov.io/gh/electricmagnetic/kakadatabase-back)

The GeoDjango-based back-end for the Kākā Database citizen science project.

Setup
-----
This guide assumes that `python3`, `pip`, `postgres` (with postgis) and virtual
environments are installed.

`./manage.py` commands should be run from the `src/` directory.

For instructions on setting up PostGIS:
<https://docs.djangoproject.com/en/2.2/ref/contrib/gis/install/postgis/>

Required packages: `binutils`, `libproj-dev`, `gdal-bin`, `postgresql-x.x`, `postgresql-x.x-postgis`, `postgresql-x.x-postgis-x.x-scripts`, `postgresql-server-dev-x.x`, `python3-psycopg2`

1. Setup `python3` virtual environment
2. Create a new database 'kakadatabase' with username 'postgres' and no password
3. `pip install -r requirements.txt`
4. `cd src`
5. `./manage.py migrate`
6. `./manage.py createsuperuser`

NB: To create database, login as postgres user then run `createdb kakadatabase` in bash shell and `grant all privileges on database kakadatabase to postgres;` in the psql shell. You may need to adjust your pg_hba.conf settings for no password access.

Running
-------
`src/manage.py runserver`

Testing
-------
Ensure that the `kakadatabase_test` db is able to be created before running.

`src/manage.py test`

You can get code coverage reports:
1. Installed `coverage` with pip
2. `coverage run src/manage.py test src`
3. `coverage report`

Importing database dump
-----------------------
To import a database dump from Heroku run the following command as the `postgres` user:
`pg_restore --clean --no-owner --role=postgres -d kakadatabase <file>.sql`

Data synchronisation: Region, Place
-----------------------------------
1. Obtain datasets for Region (merged copy of NZ regions dataset), and Place (SI-only NZ Placenames)
2. Import datasets into a local version of the database using `./manage.py loadregions` and `./manage.py loadplaces`
3. Dump data using `./manage.py dumpdata locations.place`and `./manage.py dumpdata locations.region`
4. Upload data to the database S3 bucket
5. `heroku run bash` then wget the data and run `./manage.py loaddata <filename>`

Layout
------
* `src/bands/` - Band models and helpers
* `src/birds/` - Bird models and helpers
* `src/kakadatabase/` - Project settings
* `src/locations/` - StudyArea models and helpers
* `src/observations/`- Observation models and helpers
* `src/theme/ - DRF styling, custom admin overrides for Leaflet (and template tags)

Code formatting
---------------
* Code formatting is handled by `yapf`: `yapf src/**/*.py -i`

Bug reports
-----------
Should be filed on the Kāĸā Database Trello board (not presently public)

Licence
-------
Kākā Database  
Copyright (C) 2020 Electric Magnetic Limited  

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
