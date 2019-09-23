FROM python:alpine3.7
MAINTAINER 'Jacob Dresdale'
LABEL name=plex_linker version=1.5
USER root

ENV RADARR_API_KEY=${RADARR_API_KEY}
ENV RADARR_URL=http://127.0.0.1:7878/api

ENV SONARR_API_KEY=${RADARR_API_KEY}
ENV SOANRR_URL=http://127.0.0.1:8989/api

ENV PLEX_API_KEY=${PLEX_API_KEY}
ENV PLEX_API_URL=http://127.0.0.1:32400

ENV GIT_REPO=https://github.com/jd4883/plex-linker-beta.git
ENV GIT_BRANCH=develop-docker-prototype

ENV FREQUENCY=15
ENV PLEX_LINKER=/config

ENV SONARR_ROOT_PATH_PREFIX=/
ENV YAML_FILE_CURRENT=/config/config_files/media_collection_parsed_this_run.yaml
ENV YAML_FILE_PREVIOUS=/config/config_files/media_collection_parsed_last_run.yaml
ENV LOG_NAME=plex_linker
ENV LOGS=/config/logs

ENV SEASON_INT = 0
ENV SEASON_STR = '00'
# come up with a dynamic way to dif the path from the linkers path

VOLUME /config /media
# /var/data/media
WORKDIR /config
ENV CONFIG_ARCHIVES=/config/config_files/archives
RUN apk add --no-cache bash openssh libc6-compat util-linux pciutils usbutils coreutils binutils findutils grep
COPY . /config/
RUN pip install --upgrade pip; pip install -r requirements.txt
# need to build the string a bit cleaner for this rather than use the flat 15 mins
RUN echo '*/15 *  *  *  * python /config/link-tv-specials.py' > /etc/crontabs/root; cat /etc/crontabs/root
RUN ["chmod", "+x", "/config/link-tv-specials.py"]

ENV SHOW_FOLDER_DEPTH=1
ENV MOVIE_FOLDER_DEPTH=1

ENV DOCKER_MEDIA_PATH=/media/video
ENV HOST_MEDIA_PATH=/media/video

CMD ["/usr/sbin/crond", "-f", "-d", "8"]

