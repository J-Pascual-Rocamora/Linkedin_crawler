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
		
	vars_dir = str(cwd) + r'\vars'
	if not os.path.exists(vars_dir):
		os.makedirs(vars_dir)
	
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
	
	necessary_folders = []
	
	# Create folders paths
	if sys.platform == 'win32':
		necessary_folders.append(str(cwd) + r'\log')
		necessary_folders.append(str(cwd) + r'\results')
		necessary_folders.append(str(cwd) + r'\output_texts')
		necessary_folders.append(str(cwd) + r'\Linkedin_crawler\vars')
	
	else:
		necessary_folders.append(str(cwd) + r'/log')
		necessary_folders.append(str(cwd) + r'/results')
		necessary_folders.append(str(cwd) + r'/output_texts')
		necessary_folders.append(str(cwd) + r'/Linkedin_crawler/vars')
	
	for i in range(0, len(necessary_folders)):
		if not os.path.exists(necessary_folders[i]):
			os.makedirs(necessary_folders[i])
	
	return