#/bin/bash

set -e

default_version="3"
version=${1:-"$default_version"}


# docker build -t zwarmex/woody_api:"$version" api 
# docker tag zwarmex/woody_api:"$version" zwarmex/woody_api:latest

docker build -t zwarmex/woody_rp:"$version" reverse-proxy
docker tag zwarmex/woody_rp:"$version" zwarmex/woody_rp:latest

docker build -t zwarmex/woody_database:"$version" database
docker tag zwarmex/woody_database:"$version" zwarmex/woody_database:latest

docker build -t zwarmex/woody_front:"$version" front
docker tag zwarmex/woody_front:"$version" zwarmex/woody_front:latest

# Microservices ----------------------------------
docker build -t zwarmex/woody_api_time:"$version" api-time
docker tag zwarmex/woody_api_time:"$version" zwarmex/woody_api_time:latest

docker build -t zwarmex/woody_api_heavy:"$version" api-heavy
docker tag zwarmex/woody_api_heavy:"$version" zwarmex/woody_api_heavy:latest

docker build -t zwarmex/woody_api_order:"$version" api-order
docker tag zwarmex/woody_api_order:"$version" zwarmex/woody_api_order:latest

docker build -t zwarmex/woody_api_product:"$version" api-product
docker tag zwarmex/woody_api_product:"$version" zwarmex/woody_api_product:latest
# ------------------------------------------------

# avec le "set -e" du début, je suis assuré que rien ne sera pushé si un seul build ne c'est pas bien passé

# docker push zwarmex/woody_api:"$version"
# docker push zwarmex/woody_api:latest

# Microservices ----------------------------------
docker push zwarmex/woody_api_time:"$version"
docker push zwarmex/woody_api_time:latest

docker push zwarmex/woody_api_heavy:"$version"
docker push zwarmex/woody_api_heavy:latest

docker push zwarmex/woody_api_order:"$version"
docker push zwarmex/woody_api_order:latest

docker push zwarmex/woody_api_product:"$version"
docker push zwarmex/woody_api_product:latest
# ------------------------------------------------

docker push zwarmex/woody_rp:"$version"
docker push zwarmex/woody_rp:latest

docker push zwarmex/woody_front:"$version"
docker push zwarmex/woody_front:latest

docker push zwarmex/woody_database:"$version"
docker push zwarmex/woody_database:latest
