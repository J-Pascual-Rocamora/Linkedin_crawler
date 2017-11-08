# 3rd: eliminate duplicates from people_links

import os
import sys
import logging

def minimize_people():
	'''Eliminates duplicated links on the profile pool.
	Reads the data in a list, converts the list to a set eliminating all the duplicates.
	Eliminates ducplicated links from \files\vars\people.txt. 
	Saves the sieved profiles pool on \files\vars\people_sorted.txt
	'''
	
	# Logger set up
	logging.basicConfig(filename='linkedin_crawler.log', format='%(asctime)s - %(filename)s - %(funcName)s - %(levelname)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)
	logger = logging.getLogger('Linkedin_logger')
	
	cwd = os.getcwd()
	if sys.platform == 'win32':
		input_file = str(cwd) + r'\files_data\vars\people.txt'
	else:
		input_file = str(cwd) + r'/files_data/vars/people.txt'
	f_input = open(input_file, 'r')
	people_links = []
	# Reads data in
	for line in f_input:
		people_links.append(line)
	f_input.close()

	# Eliminates duplicates
	print ('Number of links before sorting: ' + str(len(people_links)))
	min_people = list(set(people_links))
	print ('Number of links after sorting: ' + str(len(min_people)))
	
	duplicated_links = len(people_links) - len(min_people)
	
	if sys.platform == 'win32':
		output_file = str(cwd) + r'\files_data\vars\people_sorted.txt'
	else:
		output_file = str(cwd) + r'/files_data/vars/people_sorted.txt'
	f = open(output_file, 'w')
	
	# Generate output file
	for i in range(0, len(min_people)):
		f.write(str(min_people[i]))
	f.close()

	print ('Output file: ' + str(output_file))
	print ('')
	
	logger.info('%s duplicated links removed', duplicated_links)
	
	return

if __name__=="__main__":

	minimize_people()