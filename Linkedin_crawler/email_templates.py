import os

from Linkedin_crawler.inputs.titles import job_titles


def standard_update(profiles_parsed):

	email_data = []

	title   = 'Parsed ' + str(profiles_parsed) + ' profiles.'
	message = 'This is an standard update.'
	to_addr = emailing_data[0]

	email_data.append(title)
	email_data.append(message)
	email_data.append(to_addr)

	return email_data
	
def buggy_email(exceps_counter):

	email_data = []

	title   = 'Too many errors: ' + str(exceps_counter)
	message = 'Bad news, there have been ' + str(exceps_counter) + ' errors on a row.\nMight be something wrong?'
	to_addr = emailing_data[0]

	email_data.append(title)
	email_data.append(message)
	email_data.append(to_addr)
	
	return email_data

def warning_email():

	email_data = []

	title   = 'Warning email'
	message = 'More than ten consecutive errors have been found. This is worring.'
	to_addr = emailing_data[0]
	
	email_data.append(title)
	email_data.append(message)
	email_data.append(to_addr)
	
	return email_data


	
def job_done():

	email_data = []

	title   = 'Linkedin crawled has finished'
	message = 'Another run has been finished. You might want to restart the crawler.'
	to_addr = emailing_data[0]
	
	email_data.append(title)
	email_data.append(message)
	email_data.append(to_addr)
	
	return email_data