#! /bin/bash
# ./add-users.sh

usage() {
  echo "usage: $0 <docker-container> <new-users.csv>"
  echo "  To add users in the future create a csv file in the below path in the following format"
  echo "  Name,blazerid,email,clientid,scope"
  echo "  John Doe,jdoe,jdoe@site.com,scope"
  echo ""
  echo " "
  echo "Please install jq for this script to work. https://stedolan.github.io/jq/"
  echo " "
}

DOCKER_CONTAINER=$1
CSV_FILE=$2

if [[ $# -lt 2 ]]; then
  echo "❌ Error: required docker container argument and Rosalution Analysis Name"
fi

while IFS=',' read -r name userid email clientid scope; do
  if [[ "$name" == "Name" ]]; then
    continue 1
  fi

  EXISTS_STRING="db.users.countDocuments({username: \"${userid}\"});"
  exists_result=$(docker exec "$DOCKER_CONTAINER" mongosh rosalution_db --quiet --eval "'${EXISTS_STRING}'" )

  if [ "$exists_result" -gt 0 ]; then
    echo "'$userid' exists within Rosalution. Skipping 'add' operation."
    continue
  fi

  echo "Are you sure you want to add '$name' as user '$userid' to Rosalution? (yes/no): "
  read confirmation < /dev/tty

  if [ "$confirmation" != "yes" ]; then
    echo "'$name' as user '$userid' not added to Rosalution."
    continue
  fi

  hashed_password='$2b$12$xmKVVuGh6e0wP1fKellxMuOZ8HwVoogJ6W/SZpCbk0EEOA8xAsXYm'
  client_id=$(openssl rand -hex 16)
  multiline_json_print=$(cat <<EOF
{
  "username": "${userid}",
  "full_name":"${name}",
  "email":"${email}",
  "scope":"${scope}",
  "hashed_password":"${hashed_password}",
  "disabled":false,
  "client_id": "${client_id}",
  "client_secret": ""
}
EOF
)
  INSERT_STRING="db.users.insertOne(${multiline_json_print})"
  add_result=$(docker exec "$DOCKER_CONTAINER" mongosh rosalution_db --quiet --eval "'${INSERT_STRING}'" )
  echo "'$name' as user '$userid' successfully added to Rosalution."

done < "$CSV_FILE"
