#!/bin/sh
docker service rm "$(docker service list | grep plex_linker | awk '{print $2}')"
docker volume prune -f
rebuild-symlinks
make clean
make
docker rmi -f "$(docker image list | grep plex_linker | awk '{print $3}')"
rebuild-docker-stacks	# relevant to my setup please feel free to comment this out
docker service rm aggregators_pubhydra2_proxy aggregators_pubhydra2

