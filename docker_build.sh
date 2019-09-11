#!/bin/bash
source ~/.bashrc
rebuild-symlinks
# docker container rm plex_linker
docker image rm -f plex_linker
docker build --tag plex_linker .
# docker run --name plex_linker plex_linker
rebuild-docker-stacks
docker service rm aggregators_pubhydra2_proxy aggregators_pubhydra2
