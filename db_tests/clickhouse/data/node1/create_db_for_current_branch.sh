#!/bin/sh
bd_user="tes_drf_api"
db_host="localhost"
db_container="tes-api-v2_4_limitless-postgres_1"
# достаем название текущей ветки
branch=$(git rev-parse --abbrev-ref HEAD | sed 's/.*\///')
# собираем название новой бд
bd_name="$branch";
echo $bd_name
## меняем название тестовой и основной бд в файле .env
current_dir=$(pwd)
sed -i~ '/^PG_DB=/s/=.*/='"$bd_name"'/' $current_dir/.env
sed -i~ '/^PG_DB_TEST=/s/=.*/='"$bd_name"'/' $current_dir/.env
# создаем бд и наполняем ее, если ранее она не существовала
docker exec -i -e $db_host $db_container bash <<-EOSQL
  if psql $bd_name $bd_user -c '\q' 2>&1;
  then
   echo "database $bd_name exists"
  else
   createdb -U $bd_user $bd_name
   psql $bd_name < /tmp/gb.sql -U $bd_user
  fi
EOSQL
python manage.py makemigrations --merge
echo y
python manage.py migrate
echo y

#   psql $bd_name < /tmp/justplay-keycloak-tes.sql -U $bd_user
#   psql $bd_name < /tmp/justplay-keycloak-tes_23.08.22.sql -U $bd_user
#   psql $bd_name < /tmp/justplay-keycloak-tes_26.08.22_0247.sql -U $bd_user
#   psql $bd_name < /tmp/justplay-keycloak-tes_05.09.22_0280.sql -U $bd_user
#   psql $bd_name < /tmp/justplay-keycloak-tes_16.09.22_0280.sql -U $bd_user


# from test server
#   psql $bd_name < /tmp/justplay-keycloak-tes_24.08.22_big.sql -U $bd_user


#   psql $bd_name < /tmp/gb.sql -U $bd_user

#   psql $bd_name < /tmp/dfb.sql -U $bd_user
#   psql $bd_name < /tmp/dfb_22.08.22.sql -U $bd_user

#   psql $bd_name < /tmp/projectv-prod.sql -U $bd_user

#   psql $bd_name < /tmp/rush_0254_18.10.22.sql -U $bd_user

#   psql $bd_name < /tmp/predatorsleague_0278.sql -U $bd_user

#   psql $bd_name < /tmp/riot_0279_26.10.22.sql -U $bd_user

#   psql $bd_name < /tmp/werksliga-riot-test_0281_281022 -U $bd_user
#   psql $bd_name < /tmp/werksliga-riot-test_0282_081122 -U $bd_user

#   psql $bd_name < /tmp/boutgamers_0235_221122.sql -U $bd_user
