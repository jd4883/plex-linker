#!/bin/bash
# source ~/.bashrc
rebuild-symlinks
docker container rm plex_linker 2>& 1
docker image rm -f plex_linker 2>& 1
docker build --rm --tag plex_linker .
#docker run --name plex_linker plex_linker
rebuild-docker-stacks
docker service rm aggregators_pubhydra2_proxy aggregators_pubhydra2 2>& 1
