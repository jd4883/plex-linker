#!/bin/sh
docker service rm "$(docker service list | grep plex_linker | awk '{print $2}')" 2&>1
docker volume prune -f 2&>1
rebuild-symlinks 2&>1
make clean
make
docker rmi -f "$(docker image list | grep plex_linker | awk '{print $3}')" &wait 2&>1
rebuild-docker-stacks	# relevant to my setup please feel free to comment this out
docker service rm aggregators_pubhydra2_proxy aggregators_pubhydra2 2&>1

