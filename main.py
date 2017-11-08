# -*- coding: UTF-8 -*-

# Add try to emailing

import os
import sys
from selenium import webdriver
import argparse
import logging

import linkedin_crawler as linkedin_crawler
import lknd_analyzer as lknd_analyzer
import files_data.sort as sort
import files_data.match_new as match_new
import files_data.get_profiles as get_profiles
import files_data.gen_search_links as gen_search_links
import files_data.buscador as buscador
import files_data.emailing as emailing
import files_data.email_templates as email_templates
import files_data.files_manager as files_manager

# Django specific settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

# Ensure settings are read
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

# Your application specific imports
from files_data.models import *


def commandLineArgs():
    '''
    Handles the arguments
    '''
    
    parser = argparse.ArgumentParser(
									formatter_class=argparse.RawTextHelpFormatter,
									prog = "Linkedin_crawler",    
									description="""Searchs for linkedin profiles, analyse them and store the extracted information on a database""",
									)
    
    parser.add_argument('--version', action = 'version', version = 'Linkedin_crawler.py 1.0.0')
    parser.add_argument('-v',        action = 'version', version = 'Linkedin_crawler.py 1.0.0')
    
    parser.add_argument("-p", action='store', type=int,
						dest='page_number', default=25,
						help='''Number of pages per search. Default=25''')

    parser.add_argument("-D", action='store_true', dest='debugging_mode', default=False,
						help='''Enables debugging mode. Default=False''')
						
    parser.add_argument("-L", action='store_false', dest='lkn_searcher', default=True,
						help='''Disables the Linkedin search. Default=True''')
	
    parser.add_argument("-T", action='store_false', dest='terminal_file', default=True,
						help='''Disables the print redirection to a file. Defult=True''')
						
    parser.add_argument("-F", action='store_true', dest='firefox_flag', default=False,
						help='''Uses visible Firefox browser. Default=False''')
	
    return parser.parse_args()

def linkedin_search_engine(browser, pages_per_search):

	print ('*'*25)
	print ('LINKEDIN SEARCH ENGINE HAS BEEN CALLED')
	print ('*'*25)

	logging.info('Linkedin crawler is called')
	
	# Remove data from previous runs
	#linkedin_crawler.reset_files()
	
	# 1st -> Generates the linkedin search links
	gen_search_links.generate_links(pages_per_search)
	
	# 2nd -> Extracts linkedin profile links from each linkedin search link
	get_profiles.get_them(browser)
	
	# 3 -> Deletes duplicated profile links
	sort.minimize_people()
	
	return


if __name__=="__main__":
	
	
	logger_file = 'linkedin_crawler.log'
	logging.basicConfig(filename=logger_file, format='%(asctime)s - %(filename)s - %(funcName)s - %(levelname)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)
	logger = logging.getLogger('Linkedin_logger')
	
	args = commandLineArgs()
	pages_per_search   = args.page_number
	debugging_flag     = args.debugging_mode
	lnkd_search_flag   = args.lkn_searcher
	terminal_file_flag = args.terminal_file
	firefox_flag       = args.firefox_flag
	
	# Create folders if they do not exist
	files_manager.create_folders()
	
	if terminal_file_flag == True:
		cwd = os.getcwd()
		# Create path for windows or linux/mac
		if sys.platform == 'win32':
			terminal_path = str(cwd) + r'\terminal_output.out'
		else:
			terminal_path = str(cwd) + r'/terminal_output.out'
		print ('Terminal log redirected to:')
		print (terminal_path)
		terminal_output = open(terminal_path, 'w')
		sys.stdout = terminal_output
	
	logger.info('Number of search engine pages per search: %s', pages_per_search)
	logger.info('Debuggin_flag: %s', debugging_flag)
	
	# Initiate browser and log in
	if firefox_flag == True:
		browser = buscador.open_browser()
	if firefox_flag == False:
		browser = buscador.open_headless()
	buscador.logeate(browser)

	logger.info('Browser is open')
	
	# Call crawler
	if lnkd_search_flag == True:
		linkedin_search_engine(browser, pages_per_search)
	
	print ('*'*25)
	print ('INITIATING SCRAPPER')
	print ('*'*25)
	
	# Open Links_file
	cwd = os.getcwd()
	if sys.platform == 'win32':
		output_file = str(cwd) + r'\files_data\vars\people_sorted.txt'
	else:
		output_file = str(cwd) + r'/files_data/vars/people_sorted.txt'
	links_file = open(output_file, 'r')

	link_counter   = 0
	exceps_counter = 0
	old_xcp_countr = 0
	buggy_email_flag = False
	
	# Loop through all the linkedin profiles
	for line in links_file:
		url = str(line).replace('\n', '')
		try:
			# Check if link has been analyzed
			if debugging_flag == False:
				lknd_analyzer.analyse(browser, url)
			if debugging_flag == True:
				lknd_analyzer.debug_analyse(browser, url)
			print ('')
			print ('-'*25)
			print ('')
			old_xcp_countr = exceps_counter
			exceps_counter = 0
		except Exception as e:
			exceps_counter = exceps_counter + 1
			logger.error('Unable to analyse %s', url)
			logger.error(e)
			print ('ERROR: Unable to analyse ' + str(url.encode('utf-8','ignore')))
			print (e)
			print ('')
			print ('-'*25)
			print ('')
			pass
			
		link_counter = link_counter + 1
		if link_counter % 100 == 0:
			email_data = email_templates.standard_update(i)
			emailing.send_email(terminal_path, email_data[0], email_data[1], email_data[2])
			print ('email sent')
			
		if exceps_counter > 3:
			buggy_email_flag = True
			
		if (exceps_counter == 0) and (buggy_email_flag == True):
			email_data = email_templates.buggy_email(old_xcp_countr)
			emailing.send_email(terminal_path, email_data[0], email_data[1], email_data[2])
			buggy_email_flag = False
			print ('email sent')
			
		if (exceps_counter == 10) and (buggy_email_flag == False):
			email_data = email_templates.warning_email()
			emailing.send_email(terminal_path, email_data[0], email_data[1], email_data[2])
			print ('email sent')

	browser.quit()
	
	logger.info('Linkedin crawler has finished')
	
	f_path  = str(cwd) + r'\\' + logger_file
	email_data = email_templates.job_done()
	emailing.send_email(f_path,  email_data[0], email_data[1], email_data[2])
	print ('email sent')
	
	
	if terminal_file_flag == True:
		emailing.send_email(terminal_path, email_data[0], email_data[1], email_data[2])
		print ('email sent')
		terminal_output.close()
	