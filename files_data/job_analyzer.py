# -*- coding: UTF-8 -*-

import os
import sys
import time
	
def filter_jobs(job_experience, filter_type, year='0'):
	'''This function filters the jobs of a candidate.
		Recieves
		
	Parameters
	----------
	job_experience
				List of all jobs in a candidate Linkedin.
				[0] : Position
				[1] : Company
				[2] : Dates (Start - Finish)
				[3] : Time at position
				[4] : Location
				[5] : Resume
	filter_type
				String. Filter to be uesd for analysis.
				Options:
					current_jobs
					started_at
					past_jobs
	year
		String. This is an optional value. Only used for year filtering.
				
	Returns
	-------
	list
			List of jobs filtered.
				[0] : Position
				[1] : Company
				[2] : Dates (Start - Finish)
				[3] : Time at position
				[4] : Location
				[5] : Resume
		
	'''

	options = ['current_jobs',
				'started_at',
				'past_jobs']
	
	if filter_type not in options:
		print str(filter_type) + ' is not a valid value.'
		print 'Valid values are:'
		for i in range(0, len(options)):
			print options[i]
		sys.exit('filter_jobs recieved a not valid option value.')
	
	saved_positions  = []
	saved_companies  = []
	saved_dates      = []
	saved_time_spent = []
	saved_locations  = []
	saved_resumes    = []
	saved_jobs       = []

	if filter_type == 'current_jobs':
		for i in range(0, len(job_experience[2])):
			breaken_date = job_experience[2][i].split(' ')
			if 'Present' in breaken_date:
				saved_positions.append(job_experience[0][i])
				saved_companies.append(job_experience[1][i])
				saved_dates.append(job_experience[2][i])
				saved_time_spent.append(job_experience[3][i])
				saved_locations.append(job_experience[4][i])
				saved_resumes.append(job_experience[5][i])
	if filter_type == 'started_at':
		for i in range(0, len(job_experience[2])):
			breaken_date = job_experience[2][i].split(u'\xe2\u20ac\u201c ')
			breaken_start_date = breaken_date[0].split(' ')
			if year in breaken_start_date:
				saved_positions.append(job_experience[0][i])
				saved_companies.append(job_experience[1][i])
				saved_dates.append(job_experience[2][i])
				saved_time_spent.append(job_experience[3][i])
				saved_locations.append(job_experience[4][i])
				saved_resumes.append(job_experience[5][i])
	if filter_type == 'past_jobs':
		for i in range(0, len(job_experience[2])):
			breaken_date = job_experience[2][i].split(' ')
			if 'Present' not in breaken_date:
				saved_positions.append(job_experience[0][i])
				saved_companies.append(job_experience[1][i])
				saved_dates.append(job_experience[2][i])
				saved_time_spent.append(job_experience[3][i])
				saved_locations.append(job_experience[4][i])
				saved_resumes.append(job_experience[5][i])

	
	saved_jobs.append(saved_positions)
	saved_jobs.append(saved_companies)
	saved_jobs.append(saved_dates)
	saved_jobs.append(saved_time_spent)
	saved_jobs.append(saved_locations)
	saved_jobs.append(saved_resumes)
	
	return saved_jobs

def get_experience_years(job_experience):
	'''
	
	
	Parameters
	----------
	job_experience
					List of jobs, format:
						[0] : Position
						[1] : Company
						[2] : Dates (Start - Finish)
						[3] : Time at position
						[4] : Location
						[5] : Resume
	
	Returns
	-------
	float
			Total years of experience.
	
	'''

	acumulated_years_exp  = 0
	acumulated_months_exp = 0

	for i in range(0, len(job_experience[3])):
		years_exp = 0
		months_exp = 0
		if job_experience[3][i] != '':
			breaken_time = job_experience[3][i].split(' ')
			if (breaken_time[1] == 'mos') or (breaken_time[1] == 'mos'):
				months_exp = float(breaken_time[0])
				acumulated_months_exp = acumulated_months_exp + months_exp
			if (breaken_time[1] == 'yr') or (breaken_time[1] == 'yrs'):
				years_exp = float(breaken_time[0])
				acumulated_years_exp = acumulated_years_exp + years_exp
				if len(breaken_time) > 2:
					if (breaken_time[3] == 'mo') or (breaken_time[3] == 'mos'):
						months_exp = float(breaken_time[2])
						acumulated_months_exp = acumulated_months_exp + months_exp
	
	total_years_exp = acumulated_years_exp + acumulated_months_exp / 12.0

	return total_years_exp

def format_date(date_in, what_date):
	'''Recieves a job date as in Linkedin cvs. Returns a time.strptime.
	
	Parameters
	----------
	date_in
				LinkedIn date format (Mar 2017 - Jul 2017)
	what_date
				String. Possible values:
					start_date
					end_date
	Returns
	-------
	time.strptime
					Date with the format (%d/%m/%Y)
	
	'''
	
	what_date_options = ['start_date',
						  'end_date']

	if what_date.lower() not in what_date_options:
		print str(what_date_options) + ' is not a valid value.'
		print 'Valid values are:'
		for i in range(0, len(what_date_options)):
			print what_date_options[i]
		sys.exit('format_date recieved a not valid value.')
	
	months_dictionary = {
							'Jan':'31/01',
							'Feb':'28/02',
							'Mar':'31/03',
							'Apr':'30/04',
							'May':'31/05',
							'Jun':'30/06',
							'Jul':'31/07',
							'Aug':'31/08',
							'Sep':'30/09',
							'Oct':'31/10',
							'Nov':'30/11',
							'Dec':'31/12',
						}	
	
	splited_date = date_in.split(' ')
	if len(splited_date) == 1:
		formated_date = 'NULL'
	else:
		if what_date.lower() == 'start_date':
			if len(splited_date[0]) == 3:
				date_out = str(months_dictionary[splited_date[0]]) + '/' + str(splited_date[1])
			if len(splited_date[0]) == 4:
				date_out = '31/12/' + str(splited_date[0])
			if len(splited_date) == 3:
				date_out = '31/12/' + str(splited_date[0])
		if what_date.lower() == 'end_date':
			if (len(splited_date[-2]) == 3) and (splited_date[-2] in months_dictionary):
				date_out = str(months_dictionary[splited_date[-2]]) + '/' + str(splited_date[-1])
			if (len(splited_date[-2]) == 3) and (splited_date[-2] not in months_dictionary):
				date_out = '31/12/' + str(splited_date[-1])
			if (len(splited_date[-2]) > 3) and (splited_date[-1] != 'Present'):
				date_out = '31/12/' + str(splited_date[-1])
			if len(splited_date) == 3:
				date_out = '31/12/' + str(splited_date[-1])
		formated_date = time.strptime(date_out, "%d/%m/%Y")

		#if splited_date[-1] == 'Present':	
	
	
	
	return formated_date
	
	
def most_recent_job(job_experience):

	'''
	
	Parameters
	----------
	job_experience
					List of jobs, format:
						[0] : Position
						[1] : Company
						[2] : Dates (Start - Finish)
						[3] : Time at position
						[4] : Location
						[5] : Resume
	
	Returns
	-------
	list
				List with current jobs, format:
					[0] : Position
					[1] : Company
					[2] : Dates (Start - Finish)
					[3] : Time at position
					[4] : Location
					[5] : Resume
	'''

	saved_positions  = []
	saved_companies  = []
	saved_dates      = []
	saved_time_spent = []
	saved_locations  = []
	saved_resumes    = []
	saved_jobs       = []
	
	previous_date = "31/01/1900"

	current_jobs = filter_jobs(job_experience, 'current_jobs')
		
	for i in range(0, len(current_jobs[0])):
	
		formated_date = format_date(current_jobs[2][i], 'start_date')

		if formated_date > previous_date:
			previous_date = formated_date
			saved_positions  = current_jobs[0][i]
			saved_companies  = current_jobs[1][i]
			saved_dates      = current_jobs[2][i]
			saved_time_spent = current_jobs[3][i]
			saved_locations  = current_jobs[4][i]
			saved_resumes    = current_jobs[5][i]

	if previous_date != "31/01/1900":
		last_day   = previous_date.tm_mday
		last_month = previous_date.tm_mon
		last_year  = previous_date.tm_year
		last_date = str(last_day) + '/' + str(last_month) + '/' + str(last_year)
		saved_jobs.append(saved_positions)
		saved_jobs.append(saved_companies)
		saved_jobs.append(saved_dates)
		saved_jobs.append(saved_time_spent)
		saved_jobs.append(saved_locations)
		saved_jobs.append(saved_resumes)
		saved_jobs.append(last_date)
	else:
		saved_jobs.append('')
		saved_jobs.append('')
		saved_jobs.append('')
		saved_jobs.append('')
		saved_jobs.append('')
		saved_jobs.append('')
		saved_jobs.append('')
	
	return saved_jobs

def get_starting_date(input_pool, field):
	'''
	Gets the starting dates of the list passed in (either jobs or education).
	
	Parameters
	----------
	input_pool
					This could be a list with the jobs experience or a list with the education experiences.
					Jobs list:
						[0] : Position
						[1] : Company
						[2] : Dates (Start - Finish)
						[3] : Time at position
						[4] : Location
						[5] : Resume
					Education list:
						[0] : Institutions at which the studies have been developed
						[1] : Degrees title
						[2] : Fields of study
						[3] : Dates of studies
						[4] : Others. Other information displayed
						[5] : Resumes. Information about the education
					
	field
					String. This indicates what the input_pool contains (jobs or education). Possible values:
					job_experience
					education
					
	Returns
	-------
	list
					Start dates of the elements on the recieved list.
	'''


	fields_pool = ['job_experience',
					'education']

	if field.lower() not in fields_pool:
		print str(field) + ' is not a valid value'
		print 'Correct values are:'
		for i in range(0, len(fields_pool)):
			print fields_pool[i]
		sys.exit('get_starting_date recieved an incorrect value')

	if field.lower() == 'job_experience':
		date_index = 2
	if field.lower() == 'education':
		date_index = 3

	start_dates = []

	for i in range(0, len(input_pool[0])):
		start_date = format_date(input_pool[date_index][i], 'start_date')
		if start_date == 'NULL':
			start_dates.append('NULL')
		else:
			last_day   = start_date.tm_mday
			last_month = start_date.tm_mon
			last_year  = start_date.tm_year
			formated_date = str(last_day) + '/' + str(last_month) + '/' + str(last_year)
			start_dates.append(formated_date)

	return start_dates
	
def get_end_date(input_pool, field):
	'''
	Gets the end dates of the list passed in (either jobs or education).
	
	Parameters
	----------
	input_pool
					This could be a list with the jobs experience or a list with the education experiences.
					Jobs list:
						[0] : Position
						[1] : Company
						[2] : Dates (Start - Finish)
						[3] : Time at position
						[4] : Location
						[5] : Resume
					Education list:
						[0] : Institutions at which the studies have been developed
						[1] : Degrees title
						[2] : Fields of study
						[3] : Dates of studies
						[4] : Others. Other information displayed
						[5] : Resumes. Information about the education
					
	field
					String. This indicates what the input_pool contains (jobs or education). Possible values:
					job_experience
					education
					
	Returns
	-------
	list
					End dates of the elements on the recieved list.
	'''


	fields_pool = ['job_experience',
					'education']

	if field.lower() not in fields_pool:
		print str(field) + ' is not a valid value'
		print 'Correct values are:'
		for i in range(0, len(fields_pool)):
			print fields_pool[i]
		sys.exit('get_starting_date recieved an incorrect value')
					
	if field.lower() == 'job_experience':
		date_index = 2
	if field.lower() == 'education':
		date_index = 3

	end_dates = []
	
	for i in range(0, len(input_pool[0])):
		end_date = format_date(input_pool[date_index][i], 'end_date')
		if end_date == 'NULL':
			end_dates.append('NULL')
		else:
			last_day   = end_date.tm_mday
			last_month = end_date.tm_mon
			last_year  = end_date.tm_year
			formated_date = str(last_day) + '/' + str(last_month) + '/' + str(last_year)
			end_dates.append(formated_date)

	return end_dates	

def get_titles_from_name(input_string):
	'''
	Gets the accounting titles from the name line.
	
	Parameters
	----------
	input_string
					String. Name line from LinkedIn profile.
					
	Returns
	-------
	list
					Accounting titles from the name line.
	'''
	# http://www.ais-cpa.com/best-accounting-certifications/
	
	titles_pool = [ 'CPA',
					'CFA',
					'CMA',
					'EA',
					'CIA',
					'CISA',
					'CFE',
					'CGAP',
					'CBA']

	matched_titles = []
	broken_input = input_string.split(',')
	for i in range(0, len(broken_input)):
		clean_string = broken_input[i].replace(' ', '')
		if clean_string in titles_pool:
			matched_titles.append(clean_string)

	return matched_titles
	
if __name__=="__main__":
	print 'HI'