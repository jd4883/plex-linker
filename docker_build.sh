#!/bin/bash
docker container rm plex_linker
docker build --tag plex_linker .
docker run --name plex_linker plex_linker
