#! /bin/bash
# ./bundleBenchmark.sh

usage() {
  echo " "
  echo "usage: $0"
  echo " "
  echo " -p Absolute File Path to Rosalution Backend Service PyInstrument profiling"
  echo " -b Absolute File Path to K6 Metrics Summary JSON"
  echo " -o Output Directory"
  echo " -h Prints usage"
  echo " "
  echo ""
  echo " "
  exit
}

while getopts ":p:b:h" opt; do
  case $opt in
    p) pyinstrument_profiling_summary="$OPTARG";;
    b) k6_metrics_summary_json="$OPTARG";;
    h) usage;;
    \?) echo "Invalid option -$OPTARG" && exit 127;;
  esac
done

if [ ! -f "$pyinstrument_profiling_summary" ]; then
  echo "Missing pyinstrument profiling summary"
  exit 1
fi

if [ ! -f "$k6_metrics_summary_json" ]; then
  echo "Missing k6 benchmark metrics summary"
  exit 1
fi

date_stamp=$(date +"%Y-%m-%d-%s")
output_path="./benchmark-run-$date_stamp"

mkdir -p "$output_path"
mv "$pyinstrument_profiling_summary" "$output_path"
mv "$k6_metrics_summary_json" "$output_path"