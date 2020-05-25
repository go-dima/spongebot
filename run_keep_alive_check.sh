#!/bin/bash

WORKDIR=/home/dimag/spongebot
LOG_PATH=${WORKDIR}/spongebot_keep_alive.log

cd ${WORKDIR}

write_to_log () {
    date >> ${LOG_PATH}
    echo ${1} >> ${LOG_PATH}
    echo "--------------" >> ${LOG_PATH}
}

pid=$(pgrep spongebot)
if [ -z "${pid}" ]; then
    #   echo "pid is empty"
    write_to_log "spongebot is DOWN, starting..."
    nohup ${WORKDIR}/spongebot.py &
else
    #   echo "pid is NOT empty"
    if [ ! -z "${1}" ] && [ "${1}" == "verbose" ]; then
        write_to_log "spongebot is UP"
    fi
fi
