FROM python:alpine3.7
MAINTAINER 'Jacob Dresdale'
LABEL name=plex_linker version=1.5
USER root
ENV RADARR_API_KEY=${RADARR_API_KEY}
ENV SONARR_API_KEY=${RADARR_API_KEY}
ENV PLEX_API_KEY=${PLEX_API_KEY}
ENV GIT_REPO=https://github.com/jd4883/plex-linker-beta.git
ENV GIT_BRANCH=develop-docker-prototype
ENV FREQUENCY=15
ENV PLEX_LINKER=/config
VOLUME /config /media /var/data/media
WORKDIR /config
ENV CONFIG_ARCHIVES=/config/config_files/archives
# ; echo "*/5  *  *  *  * python /config/link-tv-specials.py"
RUN apk add --no-cache bash openssh &wait

COPY . /config/
RUN pip install --upgrade pip; pip install -r requirements.txt
# need to build the string a bit cleaner for this rather than use the flat 15 mins
RUN echo '*/5 *  *  *  * python /config/link-tv-specials.py' > /etc/crontabs/root; cat /etc/crontabs/root
RUN ["chmod", "+x", "/config/link-tv-specials.py"]

ENV SHOW_FOLDER_DEPTH=1
ENV MOVIE_FOLDER_DEPTH=1
ENV DOCKER_MEDIA_PATH=/media/video
ENV HOST_MEDIA_PATH=/var/data/media/video

CMD ["/usr/sbin/crond", "-f", "-d", "0"]
