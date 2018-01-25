import os
import sys

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

	searches = str(cwd) + r'\Linkedin_crawler\vars\searches_links.txt'
	f = open(searches, 'w')
	f.close()
	
	people_file = str(cwd) + r'\Linkedin_crawler\vars\people.txt'
	f = open(people_file,'w')
	f.close()
	
	people_sorted_file = str(cwd) + r'\Linkedin_crawler\vars\people_sorted.txt'
	f = open(people_sorted_file,'w')
	f.close()
	
	matched_links_file = str(cwd) + r'\Linkedin_crawler\vars\matched_links.txt'
	f = open(matched_links_file,'w')
	f.close()
	
	return
	
def create_folders():
	'''
	Checks for necessary folders and creates them if they are not created.
	'''
	
	cwd = os.getcwd()
	
	# Create folders paths
	if sys.platform == 'win32':
		log_dir      = str(cwd) + r'\log'
		results_dir  = str(cwd) + r'\results'
		output_texts = str(cwd) + r'\output_texts'
		vars_dir     = str(cwd) + '\Linkedin_crawler\vars'
	
	else:
		log_dir      = str(cwd) + r'/log'
		results_dir  = str(cwd) + r'/results'
		output_texts = str(cwd) + r'/output_texts'
		vars_dir     = str(cwd) + '/Linkedin_crawler/vars'
	
	
	if not os.path.exists(log_dir):
			os.makedirs(log_dir)
	
	if not os.path.exists(results_dir):
			os.makedirs(results_dir)
	
	return