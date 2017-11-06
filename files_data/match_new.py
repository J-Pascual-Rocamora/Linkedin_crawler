# 4th: Filter links by job changed in 2017

import re
import os
import sys
import csv
import time
import random
import logging
import buscador
import soup_handler

def profile_matchs(browser, year):
	'''Analyses linkedin profiles. Reads the profiles from \files\vars\people_sorted.txt. Checks if the profile meets the requirements. If so, the profile data is analysed and write into to different files. A csv file in \results\results.csv. A semicolon separated file \results\results.txt.

	Args:
		browser (obj): 	Actual web browser.
		year (int): Year at which current job was started.

	'''
	
	cwd = os.getcwd()
	# Open error_log file
	if sys.platform == 'win32':
		LOG_FILENAME = str(cwd) + r'\log\error_log.txt'
	else:
		LOG_FILENAME = str(cwd) + r'/log/error_log.txt'
	logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG)
	
	# Create the profiles pool from people_sorted.txt
	if sys.platform == 'win32':
		input_file = str(cwd) + r'\files_vars\people_sorted.txt'
	else:
		input_file = str(cwd) + r'/files_vars/people_sorted.txt'
	f_input = open(input_file, 'r')
	profiles = []
	for line in f_input:
		profiles.append(line)
	f_input.close()	

	# Create the csv output file
	results_csv = str(cwd) + r'\results\results.csv'
	f = open(results_csv,'wb')
	writer = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)
	writer.writerow( ('Pofile URL', 'Name', 'Job title', 'Company', 'Job started', 'Current location', 'Full resume', 'Resume without current position'))
	
	# Create the semicolon separated output file
	results_sm = str(cwd) + r'\results\results.txt'
	f2 = open(results_sm, 'w')
	f2.write('Job holder URL;Name;Business Name;Job Title;Holder Location;Job started?;Resume all words;Resume all words (without name, current job/company related information)')
	f2.write('\n')
	
	error_count = 0
	number_matchs = 0
	
	total = len(profiles)
	
	for i in range(0, total):
		print 'Analyzing (' + str(i) + '/' + str(total) + ') | ' + str(number_matchs) + ' matchs | ' + str(error_count) + ' exceptions'
		url = profiles[i]
		try:
			browser.get(url)
			time.sleep(random.uniform(2.1, 2.7))
			# Get the html of the url
			web_html = buscador.get_the_soup(browser)
			# Check if the profile meets the requirement
			match = soup_handler.match_date(web_html, year)
			if match == False:
				print '\tThe profile does not meet the requirements'
				print ''
			if match == True:
				number_matchs = number_matchs + 1
				# Extract the information of the profile and write it to output files
				try:
					print '\tThe profile meets the requirements'
					print '\tExtracting profile data...'
					# Get the header information
					info = soup_handler.get_info(web_html)
					# Get the experience information
					tbp = soup_handler.get_experience(web_html)
	
					print '\tName:            ' + str(info[0])
					print '\tActual Position: ' + str(info[1])
					print '\tActual Company:  ' + str(info[2])
					print '\tStarted:         ' + str(info[3])
					print '\tResidence:       ' + str(info[4])
					print ''
	
					# Creates the full experience text
					text_one = ''
					for i in range(0, len(tbp)):
						text_one = text_one + 'Position: ' + str(tbp[i][0]) + '\n'
						text_one = text_one + 'Company:  ' + str(tbp[i][1]) + '\n'
						text_one = text_one + 'Years:    ' + str(tbp[i][2]) + '\n'
						text_one = text_one + 'Location: ' + str(tbp[i][3]) + '\n'
						text_one = text_one + 'Text:     ' + '\n'
						text_one = text_one +  str(tbp[i][4]) + '\n'
		
					# Creates the eperience without the current employment info
					text_two = ''
					for j in range(1, len(tbp)):
						text_two = text_two + 'Position: ' + str(tbp[j][0]) + '\n'
						text_two = text_two + 'Company:  ' + str(tbp[j][1]) + '\n'
						text_two = text_two + 'Years:    ' + str(tbp[j][2]) + '\n'
						text_two = text_two + 'Location: ' + str(tbp[j][3]) + '\n'
						text_two = text_two + 'Text:     ' + '\n'
						text_two = text_two +  str(tbp[i][4]) + '\n'
		
					writer.writerow( (str(url),str(info[0]),str(info[1]),str(info[2]),str(info[3]),str(info[4]),str(text_one),str(text_two)) )
			
					# Format for ; separated file
					ptb_1 =  str(info[0])
					ptb_1.replace(';', ':')
					ptb_2 =  str(info[1])
					ptb_2.replace(';', ':')
					ptb_3 =  str(info[2])
					ptb_3.replace(';', ':')
					ptb_4 =  str(info[3])
					ptb_4.replace(';', ':')
					ptb_5 =  str(info[4])
					ptb_5.replace(';', ':')
					text_one.replace(';', ':')
					text_two.replace(';', ':')
					new_line = str(url) + ';' + ptb_1 + ';' + ptb_2 + ';' + ptb_3 + ';' + ptb_4 + ';' + ptb_5 + ';' + text_one + ';' + text_two
					f2.write(str(new_line) + '\n')

				except Exception as e:
					print 'Exception'
					error_count = error_count + 1
					print '\tCould not extract the information'
					logging.info(str(url) + '\n')
					logging.info('Could not extract information from link\n')
					logging.debug('Link number: ' + str(i) + '\n\n')
					continue
				
		except:
			print 'Exception'
			error_count = error_count + 1
			logging.info(str(url) + '\n')
			logging.info('Could not check the profile\n')
			logging.debug('Link number: ' + str(i) + '\n\n')
			continue
			
		print ""
	
	print 'Total number of matchs:     ' + str(number_matchs) + ' out of ' + str(total) + ' links'
	print 'Total number of exceptions: ' + str(error_count) + ' out of ' + str(total) + ' links'
		
	f.close()
	f2.close()
	
	print ''
	print 'Output files: ' 
	print '\t'+ str(results_csv)
	print '\t'+ str(results_sm)

	return
	
	
if __name__=="__main__":

	profile_matchs()