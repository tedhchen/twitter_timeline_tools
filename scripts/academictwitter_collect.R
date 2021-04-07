# library(devtools)
# install_github('cjbarrie/academictwitteR')
# This was done on March 28, 2021 (version 0.0.0.9000)
# A snapshot of the repo is forked to my github (tedhchen) for documentation

# Loading packages
library(configr)
library(academictwitteR)

# Loading configurations
params <- read.config(file = 'config.ini')
bt <- params$keys$bearer

# Functions
# High level wrapper that takes the .csv user file from `collect_timelines1.py`
process_users <- function(path, outpath, key, earliest = '2018-06-01T00:00:00Z'){
  infile <- read.csv(path, as.is = T, colClasses = c(user = 'character'))
  infile <- infile[as.logical(infile$short),c(1,2)]
  infile$start <-time_convert(infile$start)
  get_users(infile, outpath, key, earliest)
}

# Internal function to convert time format
time_convert <- function(times){
  mths <- sprintf('%02d', 1:12)
  names(mths) <- month.abb
  parsed_times <- paste(substr(times, 27, 30), '-',
                       mths[substr(times, 5, 7)], '-',
                       substr(times, 9, 10), 'T',
                       substr(times, 12, 19), 'z',
                       sep = '')
  parsed_times
}

# Internal function adapting code from `academictwitteR` to not reload data into R after collecting it
get_users <- function(infile, outpath, key, earliest){
  # Remove output in R
  body(get_user_tweets)[[7]] <- NULL
  # Let end time vary by user
  body(get_user_tweets)[[6]][[3]][[4]][[3]]$end_time <- substitute(end_tweets[i])
  get_user_tweets(infile$user, start_tweets = earliest, end_tweets = infile$start, bearer_token = key, data_path = outpath)
}

# Running script
users <-
outpath <-

process_city(users, outpath, bt)

# The `academictwitteR` packages doesn't yet deal well with errors, and no amendments have been made here, so be cognizant of what the underlying code is doing with what the API is returning.
