FROM python:alpine3.7
MAINTAINER 'Jacob Dresdale'
LABEL name=plex_linker version=1.5
USER root

VOLUME /config /media
WORKDIR /config
COPY requirements.txt /config/
RUN pip install --upgrade pip; pip install -r requirements.txt
RUN apk add --no-cache bash openssh libc6-compat util-linux pciutils usbutils coreutils binutils findutils grep

COPY . /config/
RUN echo '*/15 *  *  *  * python /config/link-tv-specials.py' > /etc/crontabs/root; cat /etc/crontabs/root

RUN ["chmod", "+x", "/config/link-tv-specials.py", "/config/launcher.sh"]

ENV SCRIPTS=$SCRIPTS/bin
# this may not be used and is setup specific

ENV SONARR_API_KEY =""
ENV RADARR_API_KEY=""
ENV PLEX_API_KEY=""

ENV SONARR_URL=http://127.0.0.1:8989/api
ENV PLEX_API_URL=http://127.0.0.1:32400
ENV RADARR_URL=http://127.0.0.1:7878/api

ENV GIT_REPO=https://github.com/jd4883/plex-linker-beta.git
ENV GIT_BRANCH=develop-docker-prototype

ENV FREQUENCY=15
ENV PLEX_LINKER=/config

ENV RADARR_ROOT_PATH_PREFIX=/
ENV SONARR_ROOT_PATH_PREFIX=/
ENV YAML_FILE_CURRENT=/config/config_files/media_collection_parsed_this_run.yaml
ENV YAML_FILE_PREVIOUS=/config/config_files/media_collection_parsed_last_run.yaml
ENV CONFIG_ARCHIVES=/config/config_files/archives
ENV LOG_NAME=plex_linker
ENV LOGS=/config/logs

ENV SONARR_DEFAULT_ROOT=tv
ENV RADARR_DEFAULT_ROOT=movies
ENV SEASON_INT=0
ENV SEASON_STR='00'
ENV EPISODE_PADDING=2


ENV DOCKER_MEDIA_PATH=/media/video
ENV HOST_MEDIA_PATH=/media/video

CMD ["/usr/sbin/crond", "-f", "-d", "8"]
