# Plex Linker

**Note:** this is a work in progress and documentation has been lagging behind. I'll get this updated more formally and accurately in the near future as I find time, but for now the TLDR of useful info is provided here:

**Docker Hub Download:** docker pull jb6magic/plex_linker:latest
- more tags will be added but for now I am not separating dev and master here. I'll be revising this down the line to give the option to test different versions and align naming with github

**Functional Updates:**
- While not perfect, the program works quite well in an alpine docker container. I am gradually implementing more API functionality and will be tweaking performance. I need to add in some time tracking and statistics to get a better idea of how optimizations improve performance. I currently have most sonarr / radarr API integration at least in a semi-working state and am continuing to harmonize the two into the linker.

**Plex Assist Script** - allows users to track movies with radarr and have them automatically link to the appropriate TV show as a special, regardless of directory

As a plex enthusiast, I found myself regularly consuming more disk space than preferable due to having duplications of data. Additionally, I find that anime specials are often logged in tmdb and are easier to find with radarr than with sonarr. Why not meld the two a bit better to share namespace data and be able to use links instead of separate files with no linking provided. Shouldn't the two be able to understand the linkage and use both engines to try and find the best possible files? This is where my program hopefully fills in the blanks.

Plex Linker is a homebrew project after failing to find a better solution. In my case, I've saved considerable space by using this tool, eliminated duplicates files, and have given myself more granular control of my library. This has also been a project to allow me to improve my coding skills and build upon designing frameworks.

I found this tool to be relatively unique and useful in its own way and intend to continue developing this and improving functionality and performance. I'd love to see contribution from other plex users and see how future versions of Plex Linker improve.

In the current implementation, the docker container has a 15 minute cron interval set (I plan to make this customizable in the future) to run the script. When the linker is initialized, it does the following workflow:

1. Reads in a yaml file from the config_files directory of what movie / show pairs are defined by the user. The minimal structure required for the linker to do its job is the following for the yaml file:
```'<movie>':              # movie file name as it appears in radarr
    Movie DB ID:        # ID from the moviedb. Eventually will just be parsed
    Shows:              # list of shows to map
        '<show>'        # 1 or more shows named as the sonarr root folder
            Episode ID: # EID from sonarr. Can be skipped 
                        # if the episode # and season # are included
            Episode:    # optional unless the EID is not set
            Season:     # optional unless the EID is not set
            seriesId:   # can be grabbed using the link through Sonarr
                        # will eventually just parse
            tvdbId:     # same situation as the seriesId```
2. Provided there are no errors in the above configuration, the linker will read in the following attributes from the docker configuration (denoted with a * if optional and ** if there isn't any programmed functionality quite yet to leverage the value) (these can be set as docker secrets or environmental variables. I personally use secrets for all sensitive data and a .env file for my docker configuration). Personally I prefer more flexibility with how docker containers are built so I try to leave a lot of configuration available to the end user without modifying my source code:
    - *DOCKER_MEDIA_PATH
    - *HOST_MEDIA_PATH
    - *PLEX_API_KEY
    - *SONARR_API_KEY
    - *RADARR_API_KEY
    - RADARR_URL
    - SONARR_URL
    - PLEX_URL
    - SONARR_ROOT_PATH_PREFIX
    - RADARR_ROOT_PATH_PREFIX
    - **GIT_REPO
    - **GIT_BRANCH
    - *PLEX_LINKER
    - **FREQUENCY
    - CONFIG_ARCHIVES
    - DOCKER_MEDIA_PATH
    - SONARR_DEFAULT_ROOT
    - **RADARR_DEFAULT_ROOT
    - **APPEND_TO_CRON_END
    - YAML_FILE_CURRENT
    - YAML_FILE_PREVIOUS
    - CONFIG_ARCHIVES
    - LOG_NAME
    - LOGS
    - SEASON_INT
    - SEASON_STR
    - EPISODE_PADDING
I'll aim to get more thorough descriptions to each of these going forward but for now I'm only documenting the mandatory fields and some of those that may be kind of obscure:

The main folder for the linker is set with the **PLEX_LINKER** envar. The media path as seen by the host is configured with the envar **HOST_MEDIA_PATH** and the container media path is defined with **DOCKER_MEDIA_PATH**. The API keys are all configured either as a secret or envar. The ENVAR's to set are the following **PLEX_API_KEY**, **SONARR_API_KEY**, and **RADARR_API_KEY** respectively.

    
*NOTE*: This readme is a WIP and will be updated over time. For now this just outlines what the program does, why and how it functions. There is definitely a lot of functionality that can be added using this program as a framework.
**NOTE**: I may need to adjust the source code to support both methods envar definitions as well as secrets, it may be secret specific in the current implementation. This is easy to create text files to represent the secrets in /run/secrets/<secret_name> and add the key as the only content of the file.
