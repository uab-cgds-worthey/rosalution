#! /bin/bash
# ./add-users.sh

usage() {
  echo "usage: $0 -t -c <docker-container> -p -f <new-users.csv> -h"
  echo "  Adding users to Rosalution. Either by bulk using a CSV or user prompts."
  echo ""
  echo "Options:"
  echo "  -t  Create a CSV template file in same directory"
  echo "  -c  Specify the Docker container <required>"
  echo "  -p  Prompt user for new user information"
  echo "  -f  Specify the CSV file path for bulk add users"
  echo "  -h  Display this help message"
  echo ""
  echo "Scopes available for Users arƒe: read, write"
  echo ""
  echo "CSV Document Format with Example"
  echo "-------"
  echo "name,username,email,clientid,scope"
  echo "John Doe,jdoe,jdoe@site.com,read"
  echo ""
  echo " "
  echo "Please ensure 'opensll' CLI application is installed for this script to work."
  echo " "
}


database="rosalution_db"
touch_csv_template_file=false
prompt_for_user=false
docker_container="rosalution-rosalution-db-1"
csv_filepath=""
fail=false

while getopts "tc:pf:h" opt; do
  case $opt in
    t) touch_csv_template_file=true;;
    c) docker_container="$OPTARG";;
    p) prompt_for_user=true;;
    f) csv_filepath="$OPTARG";;
    h) usage;;
    \?) echo "❌ Invalid option -$OPTARG" && fail=true;;
  esac
done

if ! openssl &> /dev/null
then
    echo "❌ Error: openssl could not be found."
    fail=true
fi

if $touch_csv_template_file; then
  echo "Creating template add users CSV in current working directory"
  add_user_template_filename="add_user_template.csv"
  if [ -f "$add_user_template_filename" ];then
    echo "ℹ️ Template '$add_user_template_filename' already exists."
  else
    cat >> "$add_user_template_filename" << END
name,username,email,clientid,scope
John Doe,jdoe,jdoe@site.com,read

END
  fi
fi

if [[ "$csv_filepath" != "" && ! -f "$csv_filepath"  ]]; then
  echo "❌ CSV '$csv_filepath' of users does not exist. Aborting add users operation."
  fail=true
fi

if [[ "$csv_filepath" != "" || $prompt_for_user ]]; then
  if ! docker ps -a --format '{{.Names}}' | grep -Eq "^${docker_container}\$"; then
    echo "❌ Container '$docker_container' does not exist. Aborting add users operation."
    fail=true
  fi
fi

if $fail; then
  exit 1
fi

function prompt_confirmation() {
  name=$1
  username=$2

  echo "Are you sure you want to add '$name' as user '$username' to Rosalution? (yes/no): "
  read -r confirmation < /dev/tty

  if [ "$confirmation" != "yes" ]; then
    return 1 # failure
  fi

  return 0 # success
}

function add_user() {
  name=$1
  username=$2
  email=$3
  scope=$4

  exists_query="db.users.countDocuments({username: \"${username}\"});"
  exists_result=$(docker exec "$docker_container" mongosh "$database" --quiet --eval "'${exists_query}'" )

  if [ "$exists_result" -gt 0 ]; then
    echo "ℹ️  User '$username' exists in Rosalution. Skipping 'add' operation."
    return 2 # Exit code indicating user exists
  fi

  if ! prompt_confirmation "$name" "$username"; then
    echo "ℹ️  User '$name' with username '$username' not added to Rosalution."
    return 1 # Exit code indicating user exists
  fi

  # Intentionally using signel quotes so that the string does not attempt to expand
  # shellcheck disable=SC2016
  hashed_password='$2b$12$xmKVVuGh6e0wP1fKellxMuOZ8HwVoogJ6W/SZpCbk0EEOA8xAsXYm'
  client_id=$(openssl rand -hex 16)
  multiline_json_print=$(cat <<EOF
{
  "username": "${username}",
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
  insert_query="db.users.insertOne(${multiline_json_print})"
  docker exec "$docker_container" mongosh "$database" --quiet --eval "'${insert_query}'"
  echo "✅ User'$name' with username '$username' successfully added to Rosalution."
  return 1
}


if [[ "$csv_filepath" != "" ]]; then
  echo "Adding users from '$csv_filepath'"
  while IFS=',' read -r name username email scope; do
    if [[ "$name" == "name" || "$name" == "" ]]; then
      continue 1
    fi

  add_user "$name" "$username" "$email" "$scope" 

  done < "$csv_filepath"
fi

if $prompt_for_user; then
  echo "Input in the upcomming prompts for add user information: "
  echo "Full Name: "
  read -r name < /dev/tty
  echo "Username: "
  read -r username < /dev/tty
  echo "Email: "
  read -r email < /dev/tty
  echo "Scope: read,write"
  read -r scope < /dev/tty

  add_user "$name" "$username" "$email" "$scope" 
fi


