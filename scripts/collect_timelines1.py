# Prep
import json, configparser, pickle, csv, logging, os
import pandas as pd
from tweepy import AppAuthHandler, API, Cursor

# Reading in configuation
params = configparser.ConfigParser()
params.read('config.ini')

# Functions
# Takes config file and returns authenticated api object
def twitter_auth(config):
	auth = AppAuthHandler(params['keys']['key'], params['keys']['secret'])
	api = API(auth, wait_on_rate_limit = True, wait_on_rate_limit_notify = True)
	return api

# Get relevant user ids
def get_ids(path, subset = None):
	df = pd.read_csv(path, header = 0, dtype = {'user': 'object', 'subset': 'object'})
	if subset != None:
		df.user = df.user[df['subset'] == subset]
	return list(df.user)

# takes user ids, and writes out a txt file wiith each user's status jsons
def get_timelines(users, api, outfolder):
	i = 0
	for user in users:
		timeline = []
		try:
			for status in Cursor(api.user_timeline, user_id = user, include_rts = True, exclude_replies = False, count = 200, tweet_mode = 'extended').items():
				timeline.append(status)
			timeline = [json.dumps(line._json) for line in timeline]
			filename = 'timeline_' + user + '.txt'
			with open(os.path.join(outfolder, filename), 'a', encoding = 'utf-8', newline = '') as outfile:
				for line in timeline:
					outfile.write(line + '\n')
		except Exception as e:
			logging.exception("Exception occurred when working with user id: " + user + '.')
		i += 1
		if i % 100 == 0:
			print('Finished ' + str(i) + ' users.')
	return None

def retry_missed_users(log, api, outfolder):
	missed = []
	with open(log, 'r') as infile:
		for line in infile:
			if 'Exception occurred when working with user id:' in line:
				missed.append(line[79:-2])
	get_timelines(missed, api, outfolder)

# Running script

# Setting up logger
logging.basicConfig(filename, filemode = 'a', format = '(%(asctime)s) %(levelname)s: %(message)s', level = logging.INFO)

# Authenticating api
api = twitter_auth(params)

# Get users from pre-parsed data
# csv file with:
# user, subset
# ..., ...
# subset is just a way to subset users from the csv file
# if subset == None, then no subsetting is performed
users = get_ids(path, subset)

# Getting timelines
get_timelines(users, api, outpath)

# Double checking errors
retry_missed_users(logfile, api, outpath)
