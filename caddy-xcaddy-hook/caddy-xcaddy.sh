#!/usr/bin/env bash
OUTPUT=$1
PLUGINS=$2
VERSION_LINE=$(pacman -Qi caddy | grep Version)              
CADDY_PKG_VERSION=$(echo ${VERSION_LINE#*":"} | xargs)
CADDY_VERSION=v${CADDY_PKG_VERSION%"-"*}
echo "Compiling Caddy ${CADDY_VERSION} into ${OUTPUT} using:"
for plugin in $(cat ${PLUGINS}); do
    echo " - ${plugin}"
done
xcaddy build ${CADDY_VERSION} --output $OUTPUT $(cat $PLUGINS | xargs  printf -- ' --with %s')  
