#! /bin/bash
# ./reset-analysis-manifest-annotate.sh

usage() {
  echo "usage: $0 <docker-container> <rosalution-analysis-name>"
  echo "  Clears an Analysis' annotation manifest to stage the analysis for a complete re-annotation using the"
  echo "  current annotation configuration. If the Rosalution analysis name has a space in it the argument must be"
  echo "  wrapped in quotes."
  echo ""
  echo "  To re-annotate the Analysis in the target Rosalution installation the terminal environment must be sourced"
  echo "  using the 'rosalutionrc.sh' script in <rosalution>/etc/api with a user's 'ROSALUTION_CLIENT_ID' and"
  echo "  'ROSALUTION_CLIENT_SECRET' Rosalution API credentials. 'ROSALUTION_BASE_URL' environment variable overides"
  echo "  the default base rosalution URL 'https://local.rosalution.cgds/rosalution'"
  echo " "
  echo "Please install jq for this script to work. https://stedolan.github.io/jq/"
  echo " "
}

BASE_URL="https://local.rosalution.cgds/rosalution"
DOCKER_CONTAINER=$1
ANALYSIS=$2

if [[ -v ROSALUTION_BASE_URL ]]; then
  BASE_URL=$ROSALUTION_BASE_URL
fi

fail=false

if ! jq --version &> /dev/null; then
  echo "❌ Error: jq could not be found. Exiting."
  fail=true
fi

if [[ $# -lt 2 ]]; then
  echo "❌ Error: required docker container argument and Rosalution Analysis Name"
  fail=true
fi

if [[ ! -v ROSALUTION_CLIENT_ID || ! -v ROSALUTION_CLIENT_SECRET ]]; then
  echo "❌ Rosalution API environment credentials 'ROSALUTION_CLIENT_ID' and/or 'ROSALUTION_CLIENT_SECRET' are not set."
  echo "   Source this shell session by sourcing the following script <rosalution-install>/etc/api/rosalutionrc.sh."
  echo ""
  echo "      source rosalutionrc.sh"
  echo ""
  fail=true
fi

target_rosalution_check=$(curl --fail -s -X 'GET' "$BASE_URL/api/heart-beat" -H 'accept: application/json' 2>&1)
if [[ $target_rosalution_check == *"Failed"* ]]; then
  echo "🌐❌ Unable to to connect to target Rosalution API at $BASE_URL"
  fail=true
fi

if $fail; then
    echo ""
    usage
    exit 1
fi

echo "🌐 Rosalution URL: $BASE_URL...$target_rosalution_check"
echo "🧬 Rosalution Analysis: $2"

##########################################
## Reset the Analysis' manifest in MongoDB
##########################################
reset_analysis_manifest_string="JSON.stringify(db.analyses.updateOne({ name: \"$ANALYSIS\" }, { \$set: {manifest: []} }));"
reset_analysis_manifest=$(docker exec "$DOCKER_CONTAINER" mongosh rosalution_db --quiet --eval "'${reset_analysis_manifest_string}'")
analysis_found=$(echo "$reset_analysis_manifest" | jq .matchedCount)
if [ "$analysis_found" -eq "1" ]; then
  echo "  ✔️  Rosalution Analysis: $2 - Manifest Reset"
else
  echo "  ❌ Rosalution Analysis: $2 not found in Roaslution's MongoDB 'rosalution_db' database in $DOCKER_CONTAINER"
  echo "Script exit..."
  exit 2
fi

#########################################
# Reannotate Analysis in Rosalution
#########################################
./annotate-analysis.sh "$ANALYSIS"
