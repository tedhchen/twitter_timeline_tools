# twitter_timeline_tools
Code to collect user timelines using a combination of Twitter's v1.1 and v2.0 APIs.

Change `config.ini.template` to `config.ini`. Then specify the data and log files, and add your Twitter credentials.
The order of using the scripts is `collect_timelines1.py` -> `time1_parser.py` -> `academictwitter_collect.R`.