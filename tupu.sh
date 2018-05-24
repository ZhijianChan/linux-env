#!/bin/bash

DEFAULT_GPU_HOSTS={50..142}
DEFAULT_BI_HOSTS=(59 88 97 127 142)
DEFAULT_UPLOAD_HOSTS=(50 54)
DEFAULT_API_HOSTS=()

# color
COLOR_RED='\033[31m'
COLOR_GREEN='\033[32m'
COLOR_DEFAULT='\033[0m'

USAGE="
Usage:
    tp [-u <username>] [-h <host>] [-c <commands>] [-J <jump_host> | -j] [options]
    tp <host> [-c <commands>]
    tp route
    tp mongo
    tp --help"

ARGS=`getopt -a -o jJ:h:u:c: -l help -- "$@"`
if [ $? != 0 ]; then
    echo "${USAGE}"
    exit 1
fi

eval set -- "${ARGS}"

host=""
jump=""
commands=""
user="duguiping"
host_prefix="172.25.52."

while true
do
    case "$1" in
        -h)
            host=$2; shift 2;;
        -u)
            user=$2; shift 2;;
        -c)
            commands=$2; shift 2;;
        -j)
            jump="-J 183.60.177.228"; shift;;
        -J)
            jump="-J $2"; shift 2;;
        --)
            shift; break;;
        --help)
            echo "${USAGE}"; exit 0;;
        *)
            echo "args error: $1"; exit 1;;
    esac
done

if [ "$1" == "route" ]; then
    sudo route delete -net 172.25.52.0/24 192.168.1.250
    sudo route add -net 172.25.52.0/24 192.168.1.250
    ssh-add -D
    ssh-add ${HOME}/.ssh/id_rsa
    exit 0;
elif [ "$1" == "mongo" ]; then
    mongo "mongodb://172.25.52.24:27300,172.25.52.26:27300,172.25.52.40:27300,172.25.52.41:27300,172.25.52.42:27300/bi"
    exit 0;
fi

if [ -z "${host}" ]; then
    host=$1
fi

for num in {1..255}
do
    if [ "${host}" == "${num}" ]; then
        host="${host_prefix}${host}"
    fi
done

# echo host=${host} user=${user} commands=${commands}
case "${host}" in
    "bi" | "gpu" | "api" | "upload")
        if [ -z "${commands}" ]; then
            echo "${COLOR_GREEN}ERROR${COLOR_DEFAULT}: commands option missing."
            exit 1
        fi
        
        hosts=""
        case "${host}" in
            "bi") hosts=${DEFAULT_BI_HOSTS[*]};;
            "gpu") hosts=${DEFAULT_GPU_HOSTS[*]};;
            "api") hosts=${DEFAULT_API_HOSTS[*]}; user="zhangjiguo";;
            "upload") hosts=${DEFAULT_UPLOAD_HOSTS[*]}; user="zhangjiguo";;
        esac

        for num in ${hosts[*]}
        do
            host="${host_prefix}${num}"
            echo -e "${COLOR_GREEN}RUNNING${COLOR_DEFAULT}: $host"
            ssh -At ${jump} ${user}@${host} "${commands}"
            echo -e "${COLOR_GREEN}FINISHED${COLOR_DEFAULT}: $host\n"
        done
        exit 0;;
    *)
        if [ -z "${commands}" ]; then
            ssh -A ${jump} ${user}@${host}
        else
            ssh -At ${jump} ${user}@${host} "${commands}"
        fi
        exit 0;;
esac
