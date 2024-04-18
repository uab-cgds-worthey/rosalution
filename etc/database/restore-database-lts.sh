#! /bin/bash
# ./restore-database-lts.sh <docker-container> clean
usage() {
  echo "usage: $0 <docker-container> clean(optional)"
  echo "  Restores an archived 'rosalution_db' MongoDB Database for Rosalution, into the specified"
  echo "  MongoDB docker container from the CGDS UAB Long Term Storage remote source 'cgdslts'."
  echo "  "
  echo "  Visit https://docs.rc.uab.edu/data_management/transfer/rclone/#setting-up-an-s3-lts-remote"
  echo "    for setup instructions for interacting with UAB LTS using rclone. Use 'cgdslts'"
  echo "    instead of 'uablts' for the remote configured in the setup instructions."
}

OPTIONAL_CLEAN=false

fail=false

if ! rclone --version &> /dev/null
then
    echo "Error: rclone could not be found."
    fail=true
fi

if [[ $# -lt 1 ]]
then
    echo "Error: required input missing."
    fail=true
fi

if [[ $# -ge 2 && "$2" == "clean" ]]
then
    OPTIONAL_CLEAN=true
fi

if $fail
then
    echo "Exiting script ..."
    usage
    exit 1
fi

DOCKER_CONTAINER=$1
TARGET_S3_REMOTE="cgdslts"

if ! rclone listremotes | grep -q "$TARGET_S3_REMOTE"
then
  echo "Missing expected '$TARGET_S3_REMOTE' rclone remote; aborting operation"
  usage
  exit 1
fi

if ! rclone lsf "$TARGET_S3_REMOTE:" | grep -q rosalution
then
  echo "Missing expected root path 'rosalution/' in bucket"
  exit 1
fi

echo "Available Rosalution Backups"
echo "------------------------------------------------------"
rclone lsf uablts:rosalution/db-backup --files-only | sort
echo "------------------------------------------------------"

echo "Which backup would you like to restore?"
read -r rosalution_db_backup

backup_absolute_path="$TARGET_S3_REMOTE:rosalution/db-backup/$rosalution_db_backup"
local_destination_directory=".rosalution-db-backups"
local_relative_backup_path="$local_destination_directory/$rosalution_db_backup"
if ! rclone lsf "$backup_absolute_path" | grep -q "$rosalution_db_backup"
then
  echo "Rosalution Backup '$backup_absolute_path' does not exist in CGDS' UAB LTS."
fi

mkdir -p .rosalution-db-backups

rclone copy -P  "$backup_absolute_path" "$local_destination_directory"

./restore-database.sh "$DOCKER_CONTAINER" "$local_relative_backup_path"

if [ "$OPTIONAL_CLEAN" = true ]
then
  echo "Removing local backup copy..."
  rm "$local_relative_backup_path"
fi

echo "Restore operation complete..."