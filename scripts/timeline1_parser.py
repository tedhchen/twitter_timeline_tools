# The purpose of this script is to determine the temporal range of each identified user's timelines
# Then for the ones that do not go as far back as June 2018, identify so R-based collection can be used
# prep
import json, os, csv, configparser
from subprocess import Popen, PIPE
from datetime import datetime

# Reading in configuation
params = configparser.ConfigParser()
params.read('config.ini')

# Functions
def parse_folder(path):
	user_stats = []
	files = os.listdir(path)
	for file in files:
		user_stats.append(parse_user(os.path.join(path, file), earliest))			
	return user_stats

def parse_user(file, earliest = datetime(2018, 6, 1)):
	with open(file, 'r') as infile:
		for line in infile:
			status = json.loads(line)
			end = status['created_at']
			user = status['user']['id_str']
			break
	p = Popen(['tail', '-1', file], shell = False, stderr = PIPE, stdout = PIPE)
	res, err = p.communicate()
	start = json.loads(res.decode())['created_at']
	startd = datetime.strptime(start, '%a %b %d %H:%M:%S %z %Y')
	if startd.date() < earliest.date(): # 
		short = 0
	else:
		short = 1
	return [user, start, end, short]

def csv_out(lst, outpath):
	with open(outpath, 'w', newline = '') as outfile:
		csvout = csv.writer(outfile)
		csvout.writerow(['user', 'start', 'end', 'short'])
		csvout.writerows(lst)

# Running script
path = #path to directory of stored timelines
parsed = parse_folder(path)
csv_out(parsed, outfile)


