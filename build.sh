#!/bin/bash

# ./build.sh
# ./build.sh --tag <BUILD_TAG> --target <BUILD_TARGET> --config <CONFIG_FILE_PATH> --npmrc <NPM_FILE_PATH> --push

##   + target <BUILD_TAG>: development or production
##   + tag <BUILD_TARGET>: version release or staging hash version, ex 1.0 or 14324a, default 'local'to, when local the CGDS Gitlab
##          image name is not used to tag build
##   + npmrc <CONFIG_FILE_PATH>: filepath to NPMRC 
##   + config <NPM_FILE_PATH>: filepath for the build arguments, default is <root>/etc/

##   + push: If present, pushes images to gitlab that were built

## Initializing our own variables
build_tag=local
target=production #base, development, production
build_configuration=etc/build/build.ini
npmrc_filepath=$HOME/.npmrc

## Flags
flag_push=false

built_images=()

while [[ $# -gt 0 ]]; do
  key="$1"

  case $key in
    --tag)
      build_tag="$2"
      shift # past argument
      shift # past value
      ;;
    --target)
      target="$2"
      shift
      shift
      ;;
    --config)
      build_configuration="$2"
      shift
      shift
      ;;
    --npmrc)
      npmrc_filepath="$2"
      shift
      shift
      ;;
    --push)
      ## If the --push flag is present. Keeps track of all the images that were built so they can be pushed 
      ## to their respective repositiries
      flag_push=true
      shift
      shift
      ;;
    *)      # unknown option
      shift
      ;;
  esac
done

echo "Build: $build_tag"
echo "Target: $target"
echo "Build Config Location: $build_configuration"
echo "npmrc file location: $npmrc_filepath"
echo ""
echo "Push images to git: $flag_push"

#################
# This function accepts a service name and parses the <docker-root>/etc/build/build.ini file for build variables
# for each respective service. It then constructs a string to be passed as a complete list of build arguements for
# the docker build to run. If there are no configuration variables, it passes back an empty string.
#
# build_args <service name>
#################
build_args() {
  local service_name=$1

  local retValue=""
  local config_vars
  local docker_args=()
  
  ## read the config provided
  config_vars="$(awk -v TARGET="${service_name}" -F ' *= *' '
  {
    if ($0 ~ /^\[.*\]$/) {
      gsub(/^\[|\]$/, "", $0)
      SECTION=$0
    } else if (($2 != "") && (SECTION==TARGET)) {
      print $1"="$2
    }
  }
  ' "${build_configuration}")"

  while IFS=' ' read -ra docker_args;  
  do
    for value in "${docker_args[@]}";
    do
      retValue+="--build-arg $value "
    done
  done <<< "$config_vars";
      
  echo "$retValue"
}

#################
# The build function accepts a service name and an optional build context constructs a docker build command to be
# run and build the entire docker image with a custom dockerfile stage, build tag, and build arguments.
#
# build <service name> <build context - optional> 
#################
pushImage(){
  for image in "${built_images[@]}"
  do
	  docker push "$image"
  done
}

#################
# The build function accepts a service name and an optional build context constructs a docker build command to be
# run and build the entire docker image with a custom dockerfile stage, build tag, and build arguments.
#
# build <service name> <build context - optional> 
#################
build(){
  local image_prefix_name="gitlab.rc.uab.edu:4567/center-for-computational-genomics-and-data-science/development/rosalution/"
  local service_name=$1
  local build_context=$2

  if [ -z "$build_context" ]
    then
      build_context="./$service_name"
  fi

  if [ "$build_tag" ==  "local" ]
    then
    image_prefix_name=""
  fi

  local image_name=$image_prefix_name$service_name:$build_tag
  local build_target=$target-stage

  local docker_args
  
  docker_args="$(build_args "$service_name")"

  # Making this a comment now to preserve code in the event we need the npmrc for future CGDS modules
  # docker_build_command="DOCKER_BUILDKIT=1 docker build --no-cache=true --secret id=npmrc,src=$npmrc_filepath --target=$build_target $(build_args "$service_name") --tag=$image_name -f ./$service_name/Dockerfile $build_context"
  docker_build_command="DOCKER_BUILDKIT=1 docker build --no-cache=true --target=$build_target $(build_args "$service_name") --tag=$image_name -f ./$service_name/Dockerfile $build_context"

  echo "Building $service_name..."
  eval "$docker_build_command"

  if [ "$flag_push" = true ]
    then
    built_images+=("$image_name")
  fi
}

buildDatabaseFixture() {
  local build_target="production-stage"
  local image_name="gitlab.rc.uab.edu:4567/center-for-computational-genomics-and-data-science/development/rosalution/database-fixture:$build_tag"
  local build_context="./etc/fixtures"
  local docker_build_command="DOCKER_BUILDKIT=1 docker build --no-cache=true --target=$build_target --tag=$image_name -f $build_context/production.Dockerfile $build_context"

  echo "Building Database Fixture..."
  eval "$docker_build_command"

  if [ "$flag_push" = true ]
    then
    built_images+=("$image_name")
  fi
}

## Frontend 
build frontend

## Backend
build backend

## Building a base database fixture for testing deployments of Rosalution
## for database
buildDatabaseFixture

if [ "$flag_push" = true ]
  then
    pushImage
fi