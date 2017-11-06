# 1st step: Generates the linkedin links from where the profiles will be extracted

import os
import sys
import logging
from titles import accounting_job_titles

def generate_links(max_pages):
	'''Generates linkedin search links. Generates a number of search pages for each job title equal to max_pages. 
	Saves the generated links on: \files\vars\searches_links.txt

	Parameters
	----------
		max_pages (int)
						Number of linkedin search pages to create.
	'''

	logging.basicConfig(filename='linkedin_crawler.log', format='%(asctime)s - %(filename)s - %(funcName)s - %(levelname)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)
	logger = logging.getLogger('Linkedin_logger')

	# Printing for tracking
	print 'The positions been looked for are:'
	for j in range(0, len(accounting_job_titles)):
		print '\t' + str(accounting_job_titles[j])

	print ''
	
	print 'Generating links...'

	url_head = 'https://www.linkedin.com/search/results/people/?facetGeoRegion=%5B%22us%3A0%22%5D&keywords='
	url_end  = '&origin=GLOBAL_SEARCH_HEADER'

	cwd = os.getcwd()
	if sys.platform == 'win32':
		output_file = str(cwd) + r'\files_data\vars\searches_links.txt'
	else:
		output_file = str(cwd) + r'/files_data/vars/searches_links.txt'
	f = open(output_file,'w')
	
	for n in range(0, len(accounting_job_titles)):
		# Create links
		tbp = accounting_job_titles[n].replace(" ", "%20")
		url = url_head + tbp + url_end
		f.write(str(url) +'\n')
		for i in range(2, max_pages):
			url_number = url + '&page=' + str(i)
			f.write(str(url_number) +'\n')
	f.close()
	
	total_links = len(accounting_job_titles) * (max_pages)
	
	logger.info('%s linkedin search links generated', total_links)
	
	print '\t' + str(total_links) + ' links generated'
	print ''
	print 'Search links are stored in: ' + str(output_file)
	print ''
	return

if __name__=="__main__":

	max_pages = 6
	generate_links(max_pages)
	