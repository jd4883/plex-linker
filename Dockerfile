FROM python:alpine3.7
MAINTAINER 'Jacob Dresdale'
LABEL name=plex_linker version=1.6
USER root

VOLUME /config /media
WORKDIR /config
COPY requirements.txt /config/
RUN pip install --upgrade pip && \
	pip install -r requirements.txt && \
	apk add --no-cache bash \
		openssh \
		libc6-compat \
		util-linux \
		pciutils \
		usbutils \
		coreutils \
		binutils \
		findutils \
		grep

ARG \
	FREQUENCY=15 \
	APPEND_TO_CRON_END=""

ENV \
	FREQUENCY=${FREQUENCY} \
	APPEND_TO_CRON_END=${APPEND_TO_CRON_END} \
	SCRIPTS=${SCRIPTS}/bin \
	CONFIG_ARCHIVES=/config/config_files/archives \
	DOCKER_MEDIA_PATH=/media/video \
	RADARR_API_KEY="" \
	GIT_BRANCH=master \
	GIT_REPO="https://github.com/jd4883/plex-linker-beta.git" \
	HOST_MEDIA_PATH=/media/video \
	LOGS=/config/logs \
	PLEX_ANIME=Anime \
	PLEX_API_KEY="" \
	PLEX_API_URL="http://127.0.0.1:32400" \
	PLEX_LINKER=/config \
	PLEX_MOVIES=Movies \
	PLEX_PASSWORD=changeMe \
	PLEX_SERVER="" \
	PLEX_SHOWS="TV Shows" \
	PLEX_URL="http://127.0.0.1:32400" \
	PLEX_USERNAME=changeMe \
	RADARR_DEFAULT_ROOT=movies \
	RADARR_ROOT_PATH_PREFIX=/ \
	RADARR_URL="http://127.0.0.1:7878/api" \
	SEASON_INT=0 \
	SEASON_STR='00' \
	SONARR_API_KEY="" \
	SONARR_DEFAULT_ROOT=tv \
	SONARR_ROOT_PATH_PREFIX=/ \
	SONARR_URL="http://127.0.0.1:8989/api" \
	YAML_FILE_CURRENT=/config/config_files/media_collection_parsed_this_run.yaml \
	YAML_FILE_PREVIOUS=/config/config_files/media_collection_parsed_last_run.yaml

COPY . /config/

RUN echo "*/${FREQUENCY} *  *  *  * python /config/link-tv-specials.py "${APPEND_TO_CRON_END}" > /etc/crontabs/root; cat /etc/crontabs/root

RUN ["chmod", "+x", "/config/link-tv-specials.py", "/config/launcher.sh"]

CMD ["/usr/sbin/crond", "-f", "-d", "8"]
