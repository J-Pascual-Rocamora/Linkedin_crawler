import os
import sys
import time
import argparse

import Linkedin_crawler.sort as sort
import Linkedin_crawler.match_new as match_new
import Linkedin_crawler.get_profiles as get_profiles
import Linkedin_crawler.gen_search_links as gen_search_links
import Linkedin_crawler.buscador as buscador


# Need to improve the flags
# Might want to put the filter as an option 


def commandLineArgs():
	'''Deals with the command line arguments

	'''
	
	parser = argparse.ArgumentParser(
	formatter_class=argparse.RawTextHelpFormatter,
	prog = "Linkedin Scrapper",
	description="""Retrieves linkedin profile information""",
	)
    
	parser.add_argument('--version', action = 'version', version = '%(prog)s 0.0.1')
	parser.add_argument('-v', action = 'version', version = '%(prog)s 0.0.1')
	
	parser.add_argument('-y', action='store', dest='year', default='2017', metavar='Year',
    help='''This is the year at which the current job was started.''')
    	
	parser.add_argument('-p', action='store', dest='pages', default='5', type=int, metavar='Pages',
    help='''How many linkedin search pages will be created for every sinlge position.''')
		
	return parser.parse_args()

def reset_files():
	'''Deletes previous information on files
	
	'''
	
	cwd = os.getcwd()
	log_dir = str(cwd) + r'\log'
	if not os.path.exists(log_dir):
		os.makedirs(log_dir)
	
	results_dir = str(cwd) + r'\results'
	if not os.path.exists(results_dir):
		os.makedirs(results_dir)
	
	error_log = log_dir + r'\error.log.txt'
	f = open(error_log, 'w')
	f.close()

	searches = str(cwd) + r'\files\vars\searches_links.txt'
	f = open(searches, 'w')
	f.close()
	
	people_file = str(cwd) + r'\files\vars\people.txt'
	f = open(people_file,'w')
	f.close()
	
	people_sorted_file = str(cwd) + r'\files\vars\people_sorted.txt'
	f = open(people_sorted_file,'w')
	f.close()
	
	matched_links_file = str(cwd) + r'\files\vars\matched_links.txt'
	f = open(matched_links_file,'w')
	f.close()
	
	return
	
	
if __name__=="__main__":

	start_time = time.time()

	# Gets the commands from the command line
	args = commandLineArgs()
	pages_per_link = args.pages
	year = args.year
	
	# Empty the output files from previous simulations
	reset_files()
	
	# Generates the linkedin search links
	gen_search_links.generate_links(pages_per_link)
	
	# Opens the internet browser
	browser = buscador.open_browser()
	buscador.logeate(browser)
	# Extracts linkedin profile links from each linkedin search link
	get_profiles.get_them(browser)
	# Deletes duplicated profile links
	sort.minimize_people()
	# Check for profiles on the pool which meet the requirement
	# and extracts the profile information
	match_new.profile_matchs(browser, year)
	
	# Close the browser
	browser.quit()
	
	end_time = time.time()
	
	total_time = end_time - start_time
	
	print ('')
	print ('Execution time: ' + str(total_time) + ' s. | ' + str(total_time/60) + ' min. | ' + str(total_time/3600) + ' h.')