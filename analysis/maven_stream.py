#!/bin/bash

handle_interrupt() {
    echo "script interrupted by user (Ctrl+C)."
    exit
}
trap 'handle_interrupt' SIGINT

usage="
$(basename "$0") [-h] [-c collection_rid] [-n stream_name] [-t] [i stream_source] -- sends stream content over srt
where:
    -h   show this help text
    -c   the collection rid for your stream (can be created with the 'create_collection.sh' script)
    -n   the name of your stream
    -t   [optional] if present, this flag indicates that a demo test stream should be used
    -i   [optional] the source of your stream (this can be an address or a file)
note: before calling this script, you should run the env_setup.sh script with 'source env_setup.sh'
"
name=
collection=
test=
source=
while getopts ':c:n:i:ht' option; do
  case "$option" in
    h) echo "$usage"
       exit
       ;;
    c) collection=$OPTARG
       ;;
    n) name=$OPTARG
       ;;
    t) test=true
       ;;
    i) source=$OPTARG
       ;;
    :) printf "missing argument for -%s\n" "$OPTARG" >&2
       echo "$usage" >&2
       exit
       ;;
   \?) printf "illegal option: -%s\n" "$OPTARG" >&2
       echo "$usage" >&2
       exit
       ;;
  esac
done
shift $((OPTIND - 1))
if [[ -z $TOKEN || -z $HOSTNAME || -z $FFMPEG ]]; then
  printf "you must set the TOKEN, HOSTNAME, and FFMPEG env variables; this can be done by running 'source env_setup.sh'" >&2
  exit
fi

if [[ -z $SRT_HOSTNAME || -z $SRT_PORT || -z $USER_ID ]]; then
  printf "you must set the SRT_HOSTNAME, SRT_PORT, and USER_ID env variables; this can be done by running 'source srt_setup.sh', which can be done as part of 'source env_setup.sh'" >&2
  exit
fi

if [[ -z $collection ]]; then
  printf "a collection rid must be specified using the -c flag" >&2
  exit
fi

if [[ -z $name ]]; then
  printf "a stream name must be specified using the -n flag" >&2
  exit
fi

if [[ -z $test && -z $source ]]; then
  printf "either the -t flag must be present to indicate the demo test stream, or a source address must be specified using the -i flag" >&2
  exit
fi

printf "\nretrieving passphrase from VIS...\n"
passphrase=$(curl -k --no-progress-meter -H "Authorization: Bearer $TOKEN" "https:/$HOSTNAME/video-ingest-service/api/srt/passphrase/$collection/$name" 2>&1) || {
  echo "failed to run retrieve passphrase command: $passphrase"
  exit
}

if [[ $passphrase == {* ]]; then
  printf "encountered an error getting passphrase:\n%s" "$passphrase" >&2
  exit
fi
passphrase=$(echo "$passphrase" | tr -d '"')

printf "retrieved passphrase; sending stream...\n\n"

if [[ -n $test ]]; then
  $FFMPEG -re -f lavfi -i testsrc=size=1280x720:rate=30 -vcodec libx264 -bf 0 -f mpegts -srt_streamid '#!::'"m=publish,c=$collection,n=$name,u=$USER_ID" "srt://$SRT_HOSTNAME:$SRT_PORT?mode=caller&passphrase=$passphrase&pbkeylen=32"
else
  $FFMPEG -re -stream_loop -1 -i "${source}" -map 0 -c copy -c:v libx264 -bf 0 -f mpegts -srt_streamid '#!::'"m=publish,c=$collection,n=$name,u=$USER_ID" "srt://$SRT_HOSTNAME:$SRT_PORT?mode=caller&passphrase=$passphrase&pbkeylen=32"
fi