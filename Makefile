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
