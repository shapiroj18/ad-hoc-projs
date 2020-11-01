#!/usr/bin/env bash
date

# -O allows us to ensure the name of the output is consistent. 
# By default wget creates numbered copies if the file already exists 
# i.e. the second run will produce deaths.csv.1 if -O is not used
wget -O /tmp/deaths.csv https://raw.githubusercontent.com/nytimes/covid-19-data/master/excess-deaths/deaths.csv
# If you are running Postgres in Docker replace "psql" below with the command 
# you used to connect to your database above

# The -c option allows us to run queries non-interactively
psql postgres -c "\copy covid_deaths from '/tmp/deaths.csv' with (format csv, header true)"
