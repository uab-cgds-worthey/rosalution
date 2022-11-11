#! /bin/bash
# ./deploy-development-prod-database.sh
usage() {
  echo "usage: $0"
  echo " "
  echo "Deploys a a Rosalution mongodb database service that mounts mongodb data to local persistent storage"
  echo "in /home/centos/rosalution/db."
  echo " "
  exit
}

sudo docker service create \
  --name rosalution-db \
  --network rosalution-network-prod \
  --env MONGO_INITDB_DATABASE=rosalution_db \
  --mount type=bind,source=/home/centos/rosalution/db,destination=/data/db \
  --placement-ref 'node.labels.traefik-public.traefik-public-certificates==true'
  mongo:5.0.9