#!/bin/sh

# Wait until MySQL is ready
while ! exec 6<>/dev/tcp/db/3306; do
    echo "Trying to connect to MySQL at 3306..."
    sleep 5
done


#!/bin/sh
until docker container exec -it mysql-container-name mysqladmin ping -P 3306 -proot | grep "mysqld is alive" ; do
  >&2 echo "MySQL is unavailable - waiting for it... 😴"
  sleep 1
done


