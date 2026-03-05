#! /bin/bash
# ./project-add-user.sh

usage() {
  echo "usage: $0 -c <docker-container> -h"
  echo "  Adding and removing Rosalution user to and from projects."
  echo ""
  echo "Options:"
  echo "  -c  Specify the Docker container <required>"
  echo "  -h  Display this help message"
  echo ""
  echo " "
}

database="rosalution_db"
docker_container="rosalution-rosalution-db-1"

while getopts "c:h" opt; do
  case $opt in
    c) docker_container="$OPTARG";;
    h) usage;;
    \?) echo "❌ Invalid option -$OPTARG" && exit 2;;
  esac
done

function print_projects_table() {
  projects_query="db.projects.find({}, { _id: { \$toString: \"\$_id\" }, name: 1 }).toArray()"
  projects_result=$(docker exec "$docker_container" mongosh "$database" --quiet --eval "'EJSON.stringify(${projects_query})'" )
  echo "=== Projects in Rosalution ==="
  echo -e "Name\t\tID"
  echo "$projects_result" | jq -r '. | map([.name, ._id])[] | if ( .[0] | length ) < 8 then join("\t\t") else join("\t") end'
}

function print_users_projects() {
  echo "Username: "
  read -r username < /dev/tty

  aggregation=$(cat <<EOF
[
  {\$match: {username: "$username"}},
  {\$lookup: {
    from: "projects",
    let: { projectIds: "\$project_ids"},
    pipeline: [
        {\$match: {
            \$expr: { \$in: ["\$_id", "\$\$projectIds"]}}
        }
    ],
    as: "projects"
  }},
  {\$unwind: "\$projects"},
  {\$replaceRoot: {
    newRoot: "\$projects"
  }},
  {\$project: { _id: { \$toString: "\$_id" }, name: 1}}
]
EOF
)
  projects_query="db.users.aggregate($aggregation).toArray()"
  projects_result=$(docker exec "$docker_container" mongosh "$database" --quiet --eval "'EJSON.stringify(${projects_query})'" )
  echo "=== User's Projects in Rosalution ==="
  echo -e "Name\t\tID"
  echo "$projects_result" | jq -r '. | map([.name, ._id])[] | if ( .[0] | length ) < 8 then join("\t\t") else join("\t") end'
}

function add_user_to_project() {
  echo "Username: "
  read -r username < /dev/tty

  echo "Provide project id to add  '$username' to in Rosalution?: "
  read -r project_id < /dev/tty

  exists_query="db.projects.countDocuments({_id: ObjectId(\"$project_id\") });"
  exists_result=$(docker exec "$docker_container" mongosh "$database" --quiet --eval "'${exists_query}'" )
  echo "$exists_result"
  if [ "$exists_result" -eq 0 ]; then
    echo "ℹ️  Project ID '$project_id' does not exist in Rosalution. Skipping 'add' operation."
    return 2
  fi

  filter="{username: \"$username\"}"
  operation=$(cat <<EOF
{
  \$addToSet: { project_ids: ObjectId("$project_id") }
}
EOF
)
  insert_query="db.users.updateOne($filter, $operation)"
  docker exec "$docker_container" mongosh "$database" --quiet --eval "'${insert_query}'"
  echo "✅ User '$username' successfully added to project Rosalution."
  return 1
}


function remove_user_from_project() {
  echo "Username: "
  read -r username < /dev/tty

  echo "Provide project id to remove  '$username' from in Rosalution?: "
  read -r project_id < /dev/tty

  filter="{username: \"$username\"}"
  operation=$(cat <<EOF
{
  \$pull: { project_ids: ObjectId("$project_id") }
}
EOF
)
  remove_query="db.users.updateOne($filter, $operation)"
  docker exec "$docker_container" mongosh "$database" --quiet --eval "'${remove_query}'"
  echo "✅ User '$username' successfully removed from project Rosalution."
  return 1
}

OPTIONS=("Show Projects" "Show User's Projects" "Add User To Project" "Remove User From Project" "Quit")

function show_menu {
  select option in "${OPTIONS[@]}"; do
    echo "$option"
    break
  done
}

PS3='Please enter your choice: '
while true; do
  option=$(show_menu)

  case $option in
    "Show Projects")
        print_projects_table
        ;;
    "Show User's Projects")
        print_users_projects
        ;;
    "Add User To Project")
        add_user_to_project
        ;;
    "Remove User From Project")
        remove_user_from_project
        ;;
   esac

  if [[ $option == "Quit" ]]; then
    break
  fi
done