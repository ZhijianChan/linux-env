#!/bin/bash

DEFAULT_GPU_HOSTS=$(seq 55 164)
DEFAULT_BI_HOSTS=(88 120 127 129 131 132 142)
DEFAULT_WEB_HOSTS=(50 54)
DEFAULT_MODEL_HOSTS=(208 209)
DEFAULT_BATCH_HOSTS=(17 18)
DEFAULT_API_HOSTS=(58 60 69 71 72 73 74 75 76 77 78 79 83 84 85 102 134 135 136)
DEFAULT_US_HOSTS=(4 35 80 90 93 105 139 143 168 187)
DEFAULT_TRAIN_HOSTS=(61 62 63 81 82)

DEFAULT_HOST_PREFIX="172.25.52."

USAGE="
Usage:
    tp [-u <username> | -z] [-h <host>] [-c <commands>] [-J <jump_host> | -j] [options]
    tp <host> [-c <commands>]
    tp route
    tp fixssh
    tp adduser [-u <username> -h <host> -k <public_key>]
    tp --help"

ARGS=`getopt -a -o zjJ:h:u:c:k: -l help -- "$@"`
if [ $? != 0 ]; then
    echo "${USAGE}"
    exit 1
fi

eval set -- "${ARGS}"

# color
COLOR_RED='\033[31m'
COLOR_GREEN='\033[32m'
COLOR_DEFAULT='\033[0m'


host=""
jump=""
commands=""
public_key=""
user="duguiping"

while true
do
    case "$1" in
        -h) host=$2; shift 2;;
        -u) user=$2; shift 2;;
        -z) user="zhangjiguo"; shift;;
        -c) commands=$2; shift 2;;
        -j) jump="-J 183.60.177.228"; shift;;
        -J) jump="-J $2"; shift 2;;
        -k) public_key=$2; shift 2;;
        --) shift; break;;
        --help) echo "${USAGE}"; exit 0;;
        *) echo "args error: $1"; exit 1;;
    esac
done

if [ "$1" == "route" ]; then
    sudo route delete -net 172.25.52.0/24 192.168.1.250
    sudo route add -net 172.25.52.0/24 192.168.1.250
    ssh-add -D
    ssh-add ${HOME}/.ssh/id_rsa
    exit 0;
fi

if [ "$1" == "fixssh" ]; then
    ssh_agent_file=$(find /tmp -path '/tmp/ssh-*' -name 'agent*' -user ${USER} 2>/dev/null)
    rm -rf ~/.ssh/ssh_auth_sock
    ln -s ${ssh_agent_file} ~/.ssh/ssh_auth_sock
    exit 0;
fi

if [ -z "${host}" ]; then
    host=$1
fi

for num in {1..255}
do
    if [ "${host}" == "${num}" ]; then
        host="${DEFAULT_HOST_PREFIX}${host}"
    fi
done

function remote_run()
{
    if [[ ${#host} -le 3 ]]; then
        host=${DEFAULT_HOST_PREFIX}${host}
    fi
    echo -e "${COLOR_GREEN}RUNNING${COLOR_DEFAULT}: $host"
    ssh -At ${jump} ${user}@${host} "${commands}"
    echo -ne "${COLOR_GREEN}FINISHED${COLOR_DEFAULT}: $host "
    for i in {1..50}; do echo -n '-'; done
    echo -e '\n'
}

case "${host}" in
    "bi" | "gpu" | "api" | "web" | "train" | "model" | "batch" | "internal")
        if [ -z "${commands}" ]; then
            echo -e "${COLOR_GREEN}ERROR${COLOR_DEFAULT}: commands option missing."
            exit 1
        fi
        
        hosts=""
        case "${host}" in
            "bi") hosts=${DEFAULT_BI_HOSTS[*]};;
            "gpu") hosts=${DEFAULT_GPU_HOSTS[*]};;
            "model") hosts=${DEFAULT_MODEL_HOSTS[*]};;
            "batch") hosts=${DEFAULT_BATCH_HOSTS[*]};;
            "api") hosts=$(curl -sS -X GET "http://172.25.52.7:8888/getGPUClients?type=api" | python -m json.tool | grep -oE '[0-9.]+'); user="zhangjiguo";;
            "train") hosts=$(curl -sS -X GET "http://172.25.52.7:8888/getGPUClients?type=train" | python -m json.tool | grep -oE '[0-9.]+'); user="zhangjiguo";;
            "web") hosts=$(curl -sS -X GET "http://172.25.52.7:8888/getGPUClients?type=web" | python -m json.tool | grep -oE '[0-9.]+'); user="zhangjiguo";;
            "internal") hosts=$(curl -sS -X GET "http://172.25.52.6:7777/getGPUClients?type=api" | python -m json.tool | grep -oE '[0-9.]+'); user="zhangjiguo";;
        esac

        for host in ${hosts[*]}
        do
            remote_run
        done
        exit 0;;
    "us")
        user=zhangjiguo
        jump="-J xyz@api-us.open.tuputech.com"
        hosts=${DEFAULT_US_HOSTS[*]}
        # hosts=(35 90 93 105 143 168 187)

        for num in ${hosts[*]}
        do
            host="10.0.3.${num}"
            remote_run
        done
        exit 0;;
    *)
        if [ -z "${commands}" ]; then
            ssh -A ${jump} ${user}@${host}
        else
            remote_run
        fi
        exit 0;;
esac
