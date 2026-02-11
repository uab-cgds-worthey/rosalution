#! /bin/bash
# ./bundleBenchmark.sh

usage() {
  echo " "
  echo "usage: $0 [options...]"
  echo " "
  echo " -r | --remote        SSH options and connection string for either SCP or SSH to retrieve rendered PyInstrument"
  echo "                      output"
  echo " -d | --docker        Target Docker container for with rendered PyInstrument output"
  echo " -p | --pyinstrument  Absolute file path to rendered PyInstrument output on target, either locally, remote,"
  echo "                      docker container, or remote and docker container"
  echo " -k | --k6            Absolute file path to K6 Metrics Summary JSON on local machine"
  echo " -o | --output        Output directory for bundled benchmark results"
  echo " -h | --help          Prints usage"
  echo " "
}

base_output_path="."

while [ $# -gt 0 ]; do
  case "$1" in
    -h|-help|--help)
      usage
      ;;

    -r|-remote|--remote)
      ssh_connection="${2:-}"
      ;;
    -d|-docker|--docker)
      docker_container="${2:-}"
      ;;
    -p|-pyinstrument|--pyinstrument)
      pyinstrument_profiling_summary="${2:-}"
      ;;
    -k|-k6|--k6)
      k6_metrics_summary_json="${2:-}"
      ;;
    -o|-output|--output)
      base_output_path="${2:-}"
      ;;
    *)
      printf "***************************\n"
      printf "* Error: Invalid argument.* %s\n" "$1"
      printf "***************************\n"
      exit 1
      ;;
  esac
  shift 2
done

using_ssh=false
using_docker=false
original_pyinstrument_profiling_summary="$pyinstrument_profiling_summary"

if [ -n "${ssh_connection}" ]; then
    using_ssh=true
fi

if [ -n "${docker_container}" ]; then
    using_docker=true
fi


if ! $using_ssh && ! $using_docker; then
  if [ ! -f "$pyinstrument_profiling_summary" ]; then
    echo "Rendered PyInstrument profiling '$pyinstrument_profiling_summary' does not exist.  Canceling bundling operation ..."
    
    usage
    exit 1
  fi
fi

if [ ! -f "$k6_metrics_summary_json" ]; then
  echo "K6 benchmark metrics summary '$k6_metrics_summary_json' does not exist.  Canceling bundling operation ..."
  
  usage
  exit 1
fi

if [[ ! -d "$base_output_path" ]]
then
    echo "Base output path '$base_output_path' does not exist.  Canceling bundling operation ..."
    echo ""

    usage
    exit 1
fi

date_stamp=$(date +"%Y-%m-%d-%s")
output_directory="benchmark-run-$date_stamp"
output_path="$base_output_path/$output_directory"
profiling_filename="${pyinstrument_profiling_summary##*/}"

mkdir -p "$output_path"

retrieve_profiling_output_command=""

if $using_ssh && ! $using_docker; then
  eval scp "$ssh_connection:$pyinstrument_profiling_summary /tmp/tmp_$profiling_filename"
  pyinstrument_profiling_summary="/tmp/tmp_$profiling_filename"
fi


if $using_docker; then
  priviledged=""
  if [[ $EUID -eq 0 ]]; then #checking if script is executing as priviledged user
    priviledged="sudo "
  fi

  retrieve_profiling_output_command="$priviledged docker cp $docker_container:$pyinstrument_profiling_summary /tmp/tmp_$profiling_filename"
  pyinstrument_profiling_summary="/tmp/tmp_$profiling_filename"
fi

if $using_ssh; then
  retrieve_profiling_output_command="ssh $ssh_connection \"$retrieve_profiling_output_command && cat /tmp/tmp_$profiling_filename\" > /tmp/tmp_$profiling_filename"
  pyinstrument_profiling_summary="/tmp/tmp_$profiling_filename"
fi

if [ -n "${retrieve_profiling_output_command}" ]; then
  eval "$retrieve_profiling_output_command"
fi

mv "$pyinstrument_profiling_summary" "$output_path"
mv "$k6_metrics_summary_json" "$output_path"
tar -czvf "$output_path.tar.gz" "$output_path"

cleanup_summaries_command=""

if $using_docker; then
  priviledged=""
  if [[ $EUID -eq 0 ]]; then #checking if script is executing as priviledged user
    priviledged="sudo "
  fi
  cleanup_summaries_command="$priviledged docker exec $docker_container rm $original_pyinstrument_profiling_summary"
fi

if $using_ssh; then
  cleanup_summaries_command="ssh $ssh_connection \"$cleanup_summaries_command\""
fi

if [ -n "${cleanup_summaries_command}" ]; then
  eval "$cleanup_summaries_command"
fi

if $using_ssh && ! $using_docker; then
  eval ssh "$ssh_connection \"rm $original_pyinstrument_profiling_summary\""
fi
