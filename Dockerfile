FROM python:alpine3.7
mkdir -p /plex_linker
mkdir -p /plex_linker/class_objects /plex_linker/config_files /plex_linker/IO /plex_linker/jobs /plex_linker/logs /plex_linker/messaging /plex_linker/movies /plex_linker/string_manipulation
COPY class_objects/* /plex_linker/class_objects/
COPY config_files/* /plex_linker/config_files/
COPY IO/* /plex_linker/IO/
COPY jobs/* /plex_linker/jobs/
COPY logs/* /plex_linker/logs/
COPY messaging/* /plex_linker/messaging/
COPY movies/* /plex_linker/
COPY string_manipulation/* /plex_linker/string_manipulation/
COPY link-tv-specials.py Dockerfile README.md requirements.txt /plex_linker/
WORKDIR /plex_linker
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
# EXPOSE 5000
CMD python ./link-tv-specials.py
