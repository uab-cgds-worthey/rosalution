#! /bin/bash
# ./backup-database-lts.sh <docker-container>
usage() {
  echo "usage: $0 <mongodb-archive>"
  echo "  Backups a local MongoDB dump archive into UAB Long Term Storage remote"
  echo "  source 'cgdslts'."
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

if [[ $# -ne 1 ]]
then
    echo "Error: required input missing."
    fail=true
fi

if $fail
then
    echo "Exiting script ..."
    usage
    exit 1
fi

TARGET_LOCAL_SOURCE_DATABASE_DUMP_FILEPATH=$1
TARGET_S3_REMOTE="uablts"

if [ ! -f $TARGET_LOCAL_SOURCE_DATABASE_DUMP_FILEPATH ]
then
    echo "Error: $TARGET_LOCAL_SOURCE_DATABASE_DUMP_FILEPATH does not exist"
    usage
    exit 1
fi

if ! rclone listremotes | grep -q "$TARGET_S3_REMOTE"
then
  echo "Missing expected '$TARGET_S3_REMOTE' rclone remote; aborting operation"
  usage
  exit 1
fi

if ! rclone lsf "$TARGET_S3_REMOTE:" | grep -q rosalution
then
  echo "Missing expected root path 'rosalution/' in bucket"
  usage
  exit 1
fi


destination_backup_path="$TARGET_S3_REMOTE:rosalution/db-backup/"
rclone copy -P  "$TARGET_LOCAL_SOURCE_DATABASE_DUMP_FILEPATH" "$destination_backup_path"

echo "Backup operation complete..."