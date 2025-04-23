#! /bin/bash
# ./rosalutionrc.sh

usage() {
  echo " "
  echo "usage: $0"
  echo " "
  echo " -u Base Rosalution URL"
  echo "    (default) https://local.rosalution.cgds/rosalution"
  echo " -h Prints usage"
  echo " "
  echo "Sources your terminal session to use Rosalution's REST API."
  echo " "
  echo "To run the annotations, please log in to Rosalution to retrieve the"
  echo "Client ID and Client Secret credentials. These can be found by"
  echo "clicking on your username or going to: <rosalution url>/rosalution/account"
  echo " "
  echo " "
  exit
}

BASE_URL="https://local.rosalution.cgds/rosalution"
unset INPUT_CLIENT_ID

while getopts ":u:i:h" opt; do
  case $opt in
    u) BASE_URL="$OPTARG";;
    i) INPUT_CLIENT_ID="$OPTARG";;
    h) usage;;
    \?) echo "Invalid option -$OPTARG" && exit 127;;
  esac
done

BASE_URL="${BASE_URL%/}"
export ROSALUTION_BASE_URL=$BASE_URL

echo "Visit '$BASE_URL/account' for API account credentials: "

if [ -z "${INPUT_CLIENT_ID+1}" ]
then
  echo "Please enter your Rosalution API Client ID for Rosalution at '$BASE_URL': "
  read -r INPUT_CLIENT_ID
  export ROSALUTION_CLIENT_ID=$INPUT_CLIENT_ID
fi

echo "Please enter your Rosalution API Client Secret for Rosalution at '$BASE_URL': "
read -sr CLIENT_SECRET_INPUT
export ROSALUTION_CLIENT_SECRET=$CLIENT_SECRET_INPUT
