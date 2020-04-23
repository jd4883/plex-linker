FROM python:alpine3.7
MAINTAINER 'Jacob Dresdale'
LABEL name=plex_linker version=1.6
USER root

VOLUME /config /media
WORKDIR /config
COPY requirements.txt /config/
RUN pip install --upgrade pip; \
	pip install -r requirements.txt \
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

ARG FREQUENCY=15
ARG APPEND_TO_CRON_END=""

ENV \
	FREQUENCY ${FREQUENCY} \
	APPEND_TO_CRON_END ${APPEND_TO_CRON_END} \
	SCRIPTS $SCRIPTS/bin \
	SONARR_API_KEY  "" \
	RADARR_API_KEY "" \
	PLEX_API_KEY "" \
	SONARR_URL http://127.0.0.1:8989/api \
	PLEX_API_URL http://127.0.0.1:32400 \
	RADARR_URL http://127.0.0.1:7878/api \
	GIT_REPO https://github.com/jd4883/plex-linker-beta.git \
	GIT_BRANCH master \
	PLEX_LINKER /config \
	RADARR_ROOT_PATH_PREFIX / \
	SONARR_ROOT_PATH_PREFIX / \
	YAML_FILE_CURRENT /config/config_files/media_collection_parsed_this_run.yaml \
	YAML_FILE_PREVIOUS /config/config_files/media_collection_parsed_last_run.yaml \
	CONFIG_ARCHIVES /config/config_files/archives \
	LOG_NAME plex_linker \
	LOGS /config/logs \
	SONARR_DEFAULT_ROOT tv \
	RADARR_DEFAULT_ROOT movies \
	SEASON_INT 0 \
	SEASON_STR '00' \
	EPISODE_PADDING 2 \
	DOCKER_MEDIA_PATH /media/video \
	HOST_MEDIA_PATH /media/video

COPY . /config/

RUN echo "*/2 *  *  *  * python /config/link-tv-specials.py" > /etc/crontabs/root; cat /etc/crontabs/root

RUN ["chmod", "+x", "/config/link-tv-specials.py", "/config/launcher.sh"]

CMD ["/usr/sbin/crond", "-f", "-d", "8"]
