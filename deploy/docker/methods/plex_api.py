"""Plex API placeholder. Not used by the link job; reserved for future watch-state or library refresh."""

# The link job only uses Sonarr/Radarr for metadata and refresh. Plex sees the symlinked files
# via its library paths. To add Plex library refresh or watch sync, use plexapi here and set
# PLEX_URL, PLEX_API_KEY (token), and optionally PLEX_USERNAME/PLEX_PASSWORD for MyPlex.
