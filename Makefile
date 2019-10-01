IMAGE_NAME := plex_linker
LOG_FILES := logs/*
VERSION := latest
REGISTRY_ADDR := jb6magic

.SILENT:clean
.PHONY: clean

push: tag
	docker push $(REGISTRY_ADDR)/$(IMAGE_NAME):$(VERSION)

tag: build
	docker tag $(IMAGE_NAME):$(VERSION) $(REGISTRY_ADDR)/$(IMAGE_NAME):$(VERSION)

build: Dockerfile
	docker build --rm -t $(IMAGE_NAME):$(VERSION) -f Dockerfile .

clean:
	find logs/ -type f -not -name "*.py" -delete &wait
	docker container prune -f
	docker image prune -f
	docker volume prune -f

#	docker service rm "$(docker service list | grep plex_linker | awk '{print $2}')" 2&>1
#	docker volume prune -f
#	rebuild-symlinks
#	rebuid-docker-stacks
#	docker rmi -f "$(docker image list | grep $(IMAGE_NAME) | awk '{print $3}')" &wait
#	rebuild-docker-stacks	# relevant to my setup please feel free to comment this out
#	docker service rm aggregators_pubhydra2_proxy aggregators_pubhydra2
	# relevant to my setup please feel free to comment this out
	####################################################################################################################

