#!/bin/bash

dir="$( cd "$( dirname "$0"  )" && pwd  )"

if [ $# -gt 0 ]; then
    case $1 in
    "edit")
        code $dir/traffic_control/config.json
        exit 1;
        ;;
    "run")
        $dir/traffic_control/traffic_control.exe -c $dir/traffic_control/config.json proxy
        exit 1;
        ;;
    *)
        echo "edit/run"
        exit 1;
        ;;
    esac
fi
