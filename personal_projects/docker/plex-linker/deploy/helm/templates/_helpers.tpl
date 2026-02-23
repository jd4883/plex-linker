{{- define "plex-linker.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- define "plex-linker.fullname" -}}
{{- default .Release.Name .Values.fullnameOverride | default (include "plex-linker.name" .) | trunc 63 | trimSuffix "-" }}
{{- end }}
