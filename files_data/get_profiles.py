# 2nd: Extracts the linkedin pofiles

import buscador
import urlparse
import logging
import re
import os
import sys
import time
import random
import sys
from bs4 import BeautifulSoup
import soup_handler
	

def get_them(browser):
	'''Get linkedin profile links. 
	Retrieves linkedin profile links from the linkedin search links, found in: \files\vars\searches_links.txt. 
	Saves the profile links into a file on: \files\vars\people.txt

	Parameters
	----------
		browser
					Driver element
	
	'''
	
	# Logger set up
	logging.basicConfig(filename='linkedin_crawler.log', format='%(asctime)s - %(filename)s - %(funcName)s - %(levelname)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)
	logger = logging.getLogger('Linkedin_logger')
	
	cwd = os.getcwd()
	if sys.platform == 'win32':
		input_file = str(cwd) + r'\files_data\vars\searches_links.txt'
	else:
		input_file = str(cwd) + r'/files_data/vars/searches_links.txt'
	f_input = open(input_file, 'r')
	
	# Read data
	job_links = []
	for line in f_input:
		job_links.append(line)
	f_input.close()
	
	if sys.platform == 'win32':
		output_file = str(cwd) + r'\files_data\vars\people.txt'
	else:
		output_file = str(cwd) + r'/files_data/vars/people.txt'
	f = open(output_file,'w')
	
	total_profiles = 0
	exceptions_count = 0
	
	for i in range(0, len(job_links)):
		print 'Analizing link (' + str(i + 1) + '/' + str(len(job_links)) + ')'
		print job_links[i]
		try:
			# Go to the search page
			browser.get(job_links[i])
			time.sleep(random.uniform(2.1, 2.7))
			# Get the url html
			web_html = buscador.get_the_soup(browser)
			# Get linkedin profile links from the html
			profiles = soup_handler.get_profiles(web_html)
			# Write profile links
			for n in range(0, len(profiles)):
				f.write(str(profiles[n]) + '\n')
			total_profiles = total_profiles + len(profiles)
			print '\tProfiles found: ' + str(len(profiles))
		except Exception, e:
			print e
			exceptions_count = exceptions_count + 1
			logger.error('Could not get profiles from %s', job_links[i])
			logger.error(e)
			continue
		print ""
	
	f.close()
	
	print 'Profile links found:        ' + str(total_profiles)
	print "Total amount of exceptions: " + str(exceptions_count)
	print 'Results saved in: '           + str(output_file)
	print ""
	logger.info('%s Linkedind profiles found', total_profiles)
	
	return
	
if __name__=="__main__":

	get_them()