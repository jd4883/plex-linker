# Plex Linker

Plex Assist Script - allows users to track movies with radarr and have them automatically link to the appropriate TV show as a special, regardless of directory

As a plex enthusiast, I found myself regularly consuming more disk space than preferable due to having duplications of data. Additionally, I find that anime specials are often logged in tmdb and are easier to find with radarr than with sonarr. Why not meld the two a bit better to share namespace data and be able to use links instead of separate files with no linking provided. Shouldn't the two be able to understand the linkage and use both engines to try and find the best possible files? This is where my program hopefully fills in the blanks.

Plex Linker is a homebrew project after failing to find a better solution. In my case, I've saved considerable space by using this tool, eliminated duplicates files, and have given myself more granular control of my library. This has also been a project to allow me to improve my coding skills and build upon designing frameworks.

I found this tool to be relatively unique and useful in its own way and intend to continue developing this and improving functionality and performance. I'd love to see contribution from other plex users and see how future versions of Plex Linker improve.

This tool is completely automated and should be run as a regular cron job, or handled with anther scheduler. This is the workflow of this program:

1. The script will first read in a yaml file from `config_files/collection_parsed_last_run.yaml`. In the current build, this file does not update. The planned feature is to have two rotated files and archive the versions behind. Essentially, this is the hierarchy I would like to have coded in long-term: \
  `config_files/` \
  `config_files/collection_parsed_last_run.yaml` \
  `config_files/collection_parsed_this_run.yaml` \
  `config_files/archive/` \
  `config_files/archive/collection_parsed_<date modified>.yaml`
2. Script parses the yaml to learn the following: \
  **a.** The Movie Title as assigned in Radarr \
  **b.** The TV Show that the movie will link to \
  **c.** The episode name as Sonarr will see it minus the extension \
  \
  As it currently stands, there is no decision making within the program, it uses a user defined list where some attributes are dynamically grabbed. I envision this using the sonarr and radarr API for the following benefits (and maybe more as ideas surface): \
  **a.** Grabbing quality profiles to validate against from Sonarr and Radarr \
  **b.** Dynamically updating information stored about episodes and movies by making intelligent predictions based on key word. I am open to other ideas for criteria that are programmatically possible to make things more dynamic \
  **c.** Once library scanning has been introduced which will add additional movies to the list, I want to use the sonarr API to compare titles to show titles, and if similar enough try to match movie titles to the show. I want to get this to a hybrid state that requires some validation or checks against a master database, rather than filling in the blanks blindly as this could be disastrous. \
  **d.** I want to use the Radarr/Sonarr API's to get statistic information about movies / shows and produce it for convenience. I want to display how much storage is saved by linking, if items are removed how much space was recovered, etc.. There are so many useful pieces of data that can be parsed easily within the given framework and stored into the master yaml 
3. I want to keep all variables as read ins from the yaml file. As it currently stands, I do not have a makefile to build an environment, but I'd like to customize this so it can be personalized to a users setup rather than matching the paradigms I use on my server.
  a. For all movie directories specified as part of the list, all subdirectories that are 1 level down will be checked for movies of interest. This is something I want to add a depth level flag to in the master yaml so that the depth can be set to match a users library. I want it to also be possible to have different show and movie depths.
  b. For all tv directories each subdirectory 1 level down will be processed for shows that match the yaml file
4. Before processing links, all current links within the subdirectories are cleared to avoid duplicates. This is considered a cleanup step and probably could be more dynamic. I deprecated the function but can re-implement it as `find /var/data/media/video/ -type l -ls -delete`, but this is not an ideal method. I'd like to add validation and a way to intelligently prune out old links if the new one changes it. Figuring keyword matching will work for this.
5. There are a few specific hard coded folder creations to correct things that in my unit testing caused the script to error. Ideally these patch type mechanisms can be sorted out and not be needed.
6. All movies are checked for a video file within their directory, if it exists then a link will be created to the given tv show provided the folder exists and is defined properly.

 Features I would like to implement down the line:
 - keyword comparisons of names between Radarr and Sonarr to determine likely matches and create YAML entries. This will depend on API integration features being implemented
 - leveraging both Radarr and Sonarr's API
 - automatic yaml generation based on each movie entry. Parsing the movies should b easy, suspect a jinja template should do the trick to loop through each movie.
 - having data read into the dictionary parsed and placed back as parsed values, and stored in the new yaml file created at the end of the programs run.
 - Automatic yaml file cleanup and organization. Would like everything to alphabetize automatically after new entries have been added, and rotate every x times (this will be a trial and error testing point but a simple one).
  - bonus points if I am able to accomplish this by separating what has been processed already and exists to what needs processing
 - eliminate the mass link deletion in favor of a more direct interaction. This requires a fair amount of logic not currently in place
 - duplicate detection and deletion mechanisms based on quality / links.
 - ability to do other link types such as one tv show to another so a crossover episode appears in all shows without separate files
 - vault integration if any authentication mechanics are implemented, this will make API key storage much more warm and fuzzy feeling than hard coding it in a yaml when the featureset is ready to work with
 - per step 2c listed above, I would like to store data points about an episode and automatically build the title rather than define it as a variable
 - Implement a working season identifier. Current episodes that are marked as S0XEXX will not work if not S00EXX due to the way its processed. **I believe this is resolved but is worth creating test cases for and unit testing**
 - add tagging capabilities to link with sonarr / radarr's API. Could easily be a yaml field and make things way more dynamic in my environment at least. Could likely integrate with API's from sites like myanimelist, thetvdb, etc.. This could become a really nifty addition if implemented right just for how well it can piggyback on this framework
 - add additional useful fields, once API integration has been completed the capabilities should skyrocket
 - add / improve logging capabilities. Would like separate logs for different event types. Need to clean up and standardize messaging and logging in general both for debugging and just to make the logging more granular in general.
 - clean up file hierarchy / structure and lock down classes to have minimal required functionality imported only
 - adding synchronization on played / unplayed between items within plex
 - add tagging to sonarr and radarr indicating exactly how the link is in place
 - implement argparse and give different flag options for running this program

Current Known Issues:
- performance boosting measures; I suspect there is a lot of room for optimization in the workflow to reduce processing time. For my rather large library the script takes about 15 minutes to run at this time
- functionality is currently disabled for reading in the users movie library, comparing it to the master list, and creating an updated version of the list. When this is done correctly and certain attributes can be parsed and checked against sonarr/radarr's api, fields like season (if applicable) would fill out on their own. 

*NOTE*: This readme is a WIP and will be updated over time. For now this just outlines what the program does, why and how it functions. There is definitely a lot of functionality that can be added using this program as a framework.
