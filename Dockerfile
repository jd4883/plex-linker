FROM python:alpine3.7
MAINTAINER 'Jacob Dresdale'
LABEL name=plex_linker version=1.5
USER root

ENV RADARR_API_KEY="${RADARR_API_KEY}"
ENV SONARR_API_KEY="${RADARR_API_KEY}"
ENV PLEX_API_KEY="${PLEX_API_KEY}"
ENV GIT_REPO="https://github.com/jd4883/plex-linker-beta.git"
ENV GIT_BRANCH="develop-docker-prototype"
VOLUME /plex_linker /media
ENV app /plex_linker
WORKDIR ${app}
RUN apk add --no-cache bash git openssh &wait
# cut clone temporarily in favor of copy as clone was not working
# recommended git clone approach online
# https://stackoverflow.com/questions/33682123/dockerfile-strategies-for-git
# or
RUN cd ${app}/; git clone git clone "https://github.com/jd4883/plex-linker-beta.git" &wait; git checkout "develop-docker-prototype"
# or
#RUN cd ${APP}; git clone ${GIT_REPO} &wait; echo 'git clone completed'
COPY . ${app}/
RUN pip install --upgrade pip; pip install -r requirements.txt
RUN ls ${app}; pwd
# ENTRYPOINT = python
CMD python ./link-tv-specials.py
