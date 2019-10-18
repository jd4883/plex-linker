#!/bin/sh
docker service rm "$(docker service list | grep plex_linker | awk '{print $2}')"  &wait
docker volume prune -f &wait
rebuild-symlinks &wait
make clean &wait
make &wait
docker rmi -f "$(docker image list | grep plex_linker | awk '{print $3}')" &wait
rebuild-docker-stacks	# relevant to my setup please feel free to comment this out
#docker service rm aggregators_pubhydra2_proxy aggregators_pubhydra2

