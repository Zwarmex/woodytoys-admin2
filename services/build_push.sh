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
docker build -t zwarmex/woody_api_misc:"$version" api-misc
docker tag zwarmex/woody_api_misc:"$version" zwarmex/woody_api_misc:latest

docker build -t zwarmex/woody_api_order:"$version" api-order
docker tag zwarmex/woody_api_order:"$version" zwarmex/woody_api_order:latest

docker build -t zwarmex/woody_api_product:"$version" api-product
docker tag zwarmex/woody_api_product:"$version" zwarmex/woody_api_product:latest
# ------------------------------------------------
# RabbitMQ

docker build -t zwarmex/woody_rabbitmq:"$version" rabbitmq
docker tag zwarmex/woody_rabbitmq:"$version" zwarmex/woody_rabbitmq:latest



# avec le "set -e" du début, je suis assuré que rien ne sera pushé si un seul build ne c'est pas bien passé

# docker push zwarmex/woody_api:"$version"
# docker push zwarmex/woody_api:latest

# Microservices ----------------------------------
docker push zwarmex/woody_api_misc:"$version"
docker push zwarmex/woody_api_misc:latest

docker push zwarmex/woody_api_order:"$version"
docker push zwarmex/woody_api_order:latest

docker push zwarmex/woody_api_product:"$version"
docker push zwarmex/woody_api_product:latest
# ------------------------------------------------
# RabbitMQ

docker push zwarmex/woody_rabbitmq:"$version"
docker push zwarmex/woody_rabbitmq:latest

docker push zwarmex/woody_rp:"$version"
docker push zwarmex/woody_rp:latest

docker push zwarmex/woody_front:"$version"
docker push zwarmex/woody_front:latest

docker push zwarmex/woody_database:"$version"
docker push zwarmex/woody_database:latest
