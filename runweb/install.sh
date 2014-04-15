#!/bin/bash

# Remove old database and resynchronize it
echo "WARNING: This will delete the entire contents of the database. Continue? (y/n)"
read c
if [ "$c" != "y" ]; then
exit
fi
if [ -f "database.db" ]; then
rm database.db
fi
manage.py syncdb <<INSTALLDB
no
INSTALLDB
