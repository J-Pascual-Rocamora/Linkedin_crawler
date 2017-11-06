# -*- coding: UTF-8 -*-

import os
import re
import sys
import time
import random
# Try with those 2 commented
#import urlparse
#import urllib2
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

import files_data.profile_html_handler as profile_html_handler
import files_data.buscador as buscador
import files_data.job_analyzer as job_analyzer

import logging

# Django specific settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

# Ensure settings are read
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

# Application specific models
from files_data.models import *

def debug_analyse(browser, url):
	
	print 'debug_analyse has been called'
	print 'Analyzing: ' + str(url.encode('utf-8', 'ignore'))
	
	accomplishment_buttons_pool = [ 'accomplishments_expand_publications',
									'accomplishments_expand_certifications',
									'accomplishments_expand_honors',
									'accomplishments_expand_languages',
									'accomplishments_expand_organizations',
									'accomplishments_expand_patents',
									'accomplishments_expand_projects',
									'accomplishments_expand_courses',
									'accomplishments_expand_test_scores']
	
	
	# Goes to desired url
	browser.get(url)
	time.sleep(random.uniform(0.7, 1.3))
	print 'URL has been open'
	# Refresh URL address
	url = browser.current_url
	print 'Current url is:'
	print url
	# Expands top summary if any
	buscador.expand_summary(browser)
	time.sleep(random.uniform(0.3, 0.5))
	# Expands other links (top left)
	buscador.expand_other_links(browser)
	time.sleep(random.uniform(0.5, 0.7))
	# Scrolls to the bottom, so every section is loaded
	buscador.scroll_to_bottom(browser)	
	# Expands sections on cv (experience, education...)
	buscador.expand_all(browser)
	
	time.sleep(random.uniform(0.3, 0.7))
	web_html = buscador.get_the_soup(browser)
	## Get info from profile main page
	header_info    = profile_html_handler.get_top_card(web_html)
	other_links    = profile_html_handler.get_other_links(web_html)
	all_experience = profile_html_handler.get_jobs(web_html)
	all_educations = profile_html_handler.get_education(web_html)
	all_volunteers = profile_html_handler.get_volunteer(web_html)
	previous_jobs  = job_analyzer.filter_jobs(all_experience, 'past_jobs')
	current_jobs    = job_analyzer.filter_jobs(all_experience, 'current_jobs')
	last_started_job = job_analyzer.most_recent_job(all_experience)
	
	## Create output file
	cwd = os.getcwd()
	if sys.platform == 'win32':
		directory = str(cwd) + r'\output_texts\\'
	else:
		directory = str(cwd) + r'/output_texts/'
	if not os.path.exists(directory):
		os.makedirs(directory)
	name_for_file = str(header_info[0].encode('utf-8', 'replace').replace(' ', '_')) + str('.txt')
	file_name = name_for_file
	path = directory + file_name
	f = open(path, 'w')
	
	print 'Creating a new output file:'
	print directory
	
	
	f.write('*'*12 + 'URL ' + '*'*12 + '\n')
	f.write(str(url.encode('utf-8', 'ignore')) + '\n' + '*'*35)
	f.write('*'*12 + ' ID ' + '*'*12 + '\n')
	f.write('Here goes the ID\n')
	
	## Arranging info for output
	
	f.write('*'*12 + ' NAME ' + '*'*12 + '\n')
	candidate_name = header_info[0]
	f.write(str(candidate_name.encode('utf-8', 'ignore')) + '\n')
	print str(candidate_name.encode('utf-8', 'ignore'))
	
	f.write('*'*12 + ' TYPE ' + '*'*12 + '\n')
	f.write('Here goes the type number \n')
	
	f.write('*'*12 + ' JOB_TITLE ' + '*'*12 + '\n')
	for n in range(0, len(current_jobs[0])):
		f.write(str(current_jobs[0][n]) + '\n')
	
	f.write('*'*12 + ' JOB_TITLE_PREV ' + '*'*12 + '\n')
	if len(previous_jobs[0]) > 0:
		job_title_prev = previous_jobs[0][0]
	else:
		job_title_prev = ''
	f.write(str(job_title_prev.encode('utf-8', 'ignore')) + '\n')
	
	f.write('*'*12 + ' COMPANY_ID ' + '*'*12 + '\n')
	f.write('Here goes the company id \n')
	
	f.write('*'*12 + ' CAPACITY_RATE ' + '*'*12 + '\n')
	f.write('Here goes the capacity rate \n')
	
	f.write('*'*12 + ' LOCATION ' + '*'*12 + '\n')
	location = []
	for n in range(0, len(current_jobs[0])):
		if current_jobs[4][n] not in location:
			location.append(current_jobs[4][n])
	if location:
		for n in range(0, len(location)):
			f.write(str(location[n].encode('utf-8', 'ignore')) + '\n')
	else:
		f.write('NULL\n')

	f.write('*'*12 + ' LOCATION_PREV_STRING ' + '*'*12 + '\n')
	last_previous_location = ''
	for i in range(0, len(previous_jobs[4])):
		last_previous_location = previous_jobs[4][i]
		if last_previous_location != '':
			break
	location_prev = last_previous_location
	if location_prev:
		f.write(str(location_prev.encode('utf-8', 'ignore')) + '\n')
	else:
		f.write('NULL\n')
	
	## Expand Skills
	buscador.expand_skills(browser)
	time.sleep(random.uniform(1.0, 1.3))
	web_html = buscador.get_the_soup(browser)
	f.write('*'*12 + ' SKILLS ' + '*'*12 + '\n')
	skills_endorsements = profile_html_handler.get_skills(web_html)
	skills = skills_endorsements[0]
	for i in range(0, len(skills)):
		f.write(str(skills[i].encode('utf-8', 'replace')) + '\n')
	if len(skills) == 0:
		f.write('NULL\n')
	
	f.write('*'*12 + ' SKILLS_ENDORSMENTS ' + '*'*12 + '\n')
	ai_endorsements = skills_endorsements[1]
	for i in range(0, len(ai_endorsements)):
		f.write(str(ai_endorsements[i].encode('utf-8', 'ignore')) + '\n')
	if len(ai_endorsements) == 0:
		f.write('NULL\n')
	
	f.write('*'*12 + ' EXPERIENCE ' + '*'*12 + '\n')
	experience = job_analyzer.get_experience_years(all_experience)
	exp_int = int(round(experience))
	f.write(str(exp_int) + '\n')
	
	f.write('*'*12 + ' DATE_CREATED ' + '*'*12 + '\n')
	f.write(str((time.strftime("%Y/%m/%d"))) + ' ' + str(time.strftime("%H:%M:%S")) + '\n')
	
	f.write('*'*12 + ' AI_JOB_STARTED ' + '*'*12 + '\n')
	ai_job_started = last_started_job[6]
	f.write(str(ai_job_started.encode('utf-8', 'ignore')) + '\n')
	
	f.write('*'*12 + ' AI_CURRENT_WORKING_STARTED ' + '*'*12 + '\n')
	ai_current_working_started = job_analyzer.get_starting_date(current_jobs, 'job_experience')
	for i in range(0, len(ai_current_working_started)):
		f.write(str(ai_current_working_started[i].encode('utf-8', 'ignore')) + '\n')
	
	f.write('*'*12 + ' AI_PREVIOUS_WORKING_STARTED ' + '*'*12 + '\n')
	ai_previous_working_started = job_analyzer.get_starting_date(previous_jobs, 'job_experience')
	for i in range(0, len(ai_previous_working_started)):
		f.write(str(ai_previous_working_started[i].encode('utf-8', 'ignore')) + '\n')
	
	f.write('*'*12 + ' AI_PREVIOUS_WORKING_FINISHED ' + '*'*12 + '\n')
	ai_previous_working_finished = job_analyzer.get_end_date(previous_jobs, 'job_experience')
	for i in range(0, len(ai_previous_working_finished)):
		f.write(str(ai_previous_working_finished[i].encode('utf-8', 'ignore')) + '\n')
	
	ai_current_job_title = []
	ai_current_company = []
	ai_current_locations = []
	ai_current_working_content = []
	for j in range(0, len(current_jobs[0])):
		ai_current_job_title.append(current_jobs[0][j])	
		ai_current_company.append(current_jobs[1][j])
		ai_current_locations.append(current_jobs[4][j])
		ai_current_working_content.append(current_jobs[5][j])
		
	ai_previous_job_title = []
	ai_previous_company = []
	ai_previoius_locations = []
	ai_previous_working_content = []
	for k in range(0 , len(previous_jobs[0])):
		ai_previous_job_title.append(previous_jobs[0][k])
		ai_previous_company.append(previous_jobs[1][k])
		ai_previoius_locations.append(previous_jobs[4][k])
		ai_previous_working_content.append(previous_jobs[5][k])
	
	f.write('*'*12 + ' AI_CURRENT_JOB_TITLE ' + '*'*12 + '\n')
	for i in range(0, len(ai_current_job_title)):
		f.write(str(ai_current_job_title[i].encode('utf-8', 'ignore')) + '\n')
	
	f.write('*'*12 + ' AI_PREVIOUS_JOB_TITLE ' + '*'*12 + '\n')
	for i in range(0, len(ai_previous_job_title)):
		f.write(str(ai_previous_job_title[i].encode('utf-8', 'ignore')) + '\n')
	
	f.write('*'*12 + ' AI_CURRENT_COMPANY ' + '*'*12 + '\n')
	for i in range(0, len(ai_current_company)):
		f.write(str(ai_current_company[i].encode('utf-8', 'ignore')) + '\n')
		
	f.write('*'*12 + ' AI_PREVIOUS_COMPANY ' + '*'*12 + '\n')
	for i in range(0, len(ai_previous_company)):
		f.write(str(ai_previous_company[i].encode('utf-8', 'ignore')) + '\n')
		
	f.write('*'*12 + ' AI_CURRENT_LOCATIONS ' + '*'*12 + '\n')
	current_location_flag = False
	for i in range(0, len(ai_current_locations)):
		if ai_current_locations[i]:
			current_location_flag = True
			f.write(str(ai_current_locations[i].encode('utf-8', 'ignore')) + '\n')
	if current_location_flag == False:
		f.write('NULL\n')
		
	f.write('*'*12 + ' AI_PREVIOUS_LOCATIONS ' + '*'*12 + '\n')
	previous_locations_flag = False
	for i in range(0, len(ai_previoius_locations)):
		if ai_previoius_locations[i]:
			previous_locations_flag = True
			f.write(str(ai_previoius_locations[i].encode('utf-8', 'ignore')) + '\n')
	if previous_locations_flag == False:
		f.write('NULL\n')
	
	f.write('*'*12 + ' AI_CURRENT_WORKING_CONTENT ' + '*'*12 + '\n')
	current_working_content_text = ''
	current_working_content_flag = False
	for i in range(0, len(ai_current_working_content)):
		if ai_current_working_content[i]:
			current_working_content_flag = True
			f.write(str(ai_current_working_content[i].encode('utf-8', 'ignore')) + '\n')
			current_working_content_text = current_working_content_text + str(ai_current_working_content[i].encode('utf-8', 'ignore')) + '\n'
			if i < len(ai_current_working_content):
				f.write('+-+-+-+-+-\n')
				current_working_content_text = current_working_content_text + '+-+-+-+-+-\n'
	if current_working_content_flag == False:
		f.write('NULL\n')
		
	f.write('*'*12 + ' AI_PREVIOUS_WORKING_CONTENT ' + '*'*12 + '\n')
	previous_working_content_text = ''
	previous_working_content_flag = False
	for i in range(0, len(ai_previous_working_content)):
		if ai_previous_working_content[i]:
			previous_working_content_flag = True
			f.write(str(ai_previous_working_content[i].encode('utf-8', 'ignore')) + '\n')
			previous_working_content_text = previous_working_content_text + str(ai_previous_working_content[i].encode('utf-8', 'ignore')) + '\n'
			if i < len(ai_previous_working_content):
				f.write('+-+-+-+-+-\n')
				previous_working_content_text = previous_working_content_text + '+-+-+-+-+-\n'
	if previous_working_content_flag == False:
		f.write('NULL\n')
	
	f.write('*'*12 + ' AI_COMPANY ' + '*'*12 + '\n')
	ai_company = last_started_job[1]
	f.write(str(ai_company.encode('utf-8', 'ignore')) + '\n')
		
	f.write('*'*12 + ' AI_EDUCATION ' + '*'*12 + '\n')
	ai_education = str(all_educations[0][0].encode('utf-8', 'ignore'))
	f.write(str(ai_education) + '\n')
		
	ai_previous_education       = []
	ai_previous_degree          = []
	ai_previous_education_field = []
	for i in range(0, len(all_educations[0])):
		if all_educations[0][i] != '':
			ai_previous_education.append(all_educations[0][i])
		if all_educations[1][i] != '':
			ai_previous_degree.append(all_educations[1][i])
		if all_educations[2][i] != '':
			ai_previous_education_field.append(all_educations[2][i])
	
	f.write('*'*12 + ' AI_PREVIOUS_EDUCATION ' + '*'*12 + '\n')
	f.write(str(ai_previous_education) + '\n')
	
	f.write('*'*12 + ' AI_DEGREE ' + '*'*12 + '\n')
	ai_degree = str(all_educations[1][0].encode('utf-8', 'ignore'))
	f.write(str(ai_degree) + '\n')
	
	f.write('*'*12 + ' AI_PREVIOUS_DEGREE ' + '*'*12 + '\n')
	f.write(str(ai_previous_degree) + '\n')
	
	f.write('*'*12 + ' AI_EDUCATION_FIELD ' + '*'*12 + '\n')
	ai_education_field = str(all_educations[2][0].encode('utf-8', 'ignore'))
	f.write(str(ai_education_field.encode('utf-8', 'ignore')) + '\n')
	
	f.write('*'*12 + ' AI_PREVIOUS_EDUCATION_FIELD ' + '*'*12 + '\n')
	f.write(str(ai_previous_education_field) + '\n')
		
	f.write('*'*12 + ' AI_EDUCATION_START ' + '*'*12 + '\n')
	ai_education_start = job_analyzer.get_starting_date(all_educations, 'education')
	for i in range(0, len(ai_education_start)):
		f.write(str(ai_education_start[i]) + '\n')
	
	# 37 -> If the candidates stills studying, ai_education_finished = NULL or only current studies?
	f.write('*'*12 + ' AI_EDUCATION_FINISHED ' + '*'*12 + '\n')
	ai_education_finished = job_analyzer.get_end_date(all_educations, 'education')
	for i in range(0, len(ai_education_finished)):
		f.write(str(ai_education_finished[i]) + '\n')
	
	f.write('*'*12 + ' AI_SELF_INTRO ' + '*'*12 + '\n')
	ai_self_intro = header_info[8]
	if ai_self_intro:
		f.write(str(ai_self_intro.encode('utf-8', 'ignore')) + '\n')
	else:
		f.write('NULL\n')
	
	ai_volunteer_experience = ''
	for m in range(0, len(all_volunteers[0])):
		ai_volunteer_experience = ai_volunteer_experience + str(all_volunteers[0][m].encode('utf-8', 'ignore')) + '\n'
		ai_volunteer_experience = ai_volunteer_experience + str(all_volunteers[1][m].encode('utf-8', 'ignore')) + '\n'
		ai_volunteer_experience = ai_volunteer_experience + str(all_volunteers[2][m].encode('utf-8', 'ignore')) + '\n'
		ai_volunteer_experience = ai_volunteer_experience + str(all_volunteers[3][m].encode('utf-8', 'ignore')) + '\n'
		ai_volunteer_experience = ai_volunteer_experience + str(all_volunteers[4][m].encode('utf-8', 'ignore')) + '\n'
		ai_volunteer_experience = ai_volunteer_experience + str(all_volunteers[5][m].encode('utf-8', 'ignore')) + '\n'
		ai_volunteer_experience = ai_volunteer_experience + '\n+-+-+-+-+-\n'
	
	f.write('*'*12 + ' AI_VOLUNTEER_EXPERIENCE ' + '*'*12 + '\n')
	if ai_volunteer_experience != '':
		f.write(str(ai_volunteer_experience) + '\n')
	else:
		f.write('NULL\n')
	
	## Recommendations block
	recomendation_buttons_names = profile_html_handler.get_recommendation_buttons(web_html)
	received_number = re.findall(r'\d+', str(recomendation_buttons_names[0]))
	given_number    = re.findall(r'\d+', str(recomendation_buttons_names[1]))
	print 'Recieved recss: ' + str(received_number[0])
	print 'Given recsssss: ' + str(given_number[0])
	
	## Open recieved recomendations
	buscador.open_received_recommendations(browser)
	time.sleep(random.uniform(0.2, 0.4))
	web_html = buscador.get_the_soup(browser)
	f.write('*'*12 + ' RECOMMENDATION_RECEIVED ' + '*'*12 + '\n')
	recommendation_received_text = ''
	if received_number[0] != '0':
		all_received_rec = profile_html_handler.get_recommendations(web_html, 0)
		for n in range(0, len(all_received_rec[0])):
			f.write(str(all_received_rec[0][n].encode('utf-8', 'ignore')) + '\n')
			f.write(str(all_received_rec[1][n].encode('utf-8', 'ignore')) + '\n')
			f.write(str(all_received_rec[2][n].encode('utf-8', 'ignore')) + '\n')
			f.write(str(all_received_rec[3][n].encode('utf-8', 'ignore')) + '\n')
			recommendation_received_text = recommendation_received_text + str(all_received_rec[0][n].encode('utf-8', 'ignore')) + '\n'
			recommendation_received_text = recommendation_received_text + str(all_received_rec[1][n].encode('utf-8', 'ignore')) + '\n'
			recommendation_received_text = recommendation_received_text + str(all_received_rec[2][n].encode('utf-8', 'ignore')) + '\n'
			recommendation_received_text = recommendation_received_text + str(all_received_rec[3][n].encode('utf-8', 'ignore')) + '\n'
			if n < (len(all_received_rec[0]) - 1):
				f.write('+-+-+-+-+-\n')
				recommendation_received_text = recommendation_received_text + '+-+-+-+-+-\n'
		if len(all_received_rec) == 0:
			f.write('NULL\n')
	else:
		f.write('NULL\n')
			
	## Open given recommendations
	buscador.open_given_recommendations(browser)
	time.sleep(random.uniform(0.2, 0.4))
	web_html = buscador.get_the_soup(browser)
	f.write('*'*12 + ' RECOMMENDATION_GIVEN ' + '*'*12 + '\n')
	recommendation_given_text = ''
	if given_number[0] != '0':
		if (received_number[0] != '0') and (given_number[0] != '0'):
			block_number = 1
		else:
			block_number = 0
		all_given_rec = profile_html_handler.get_recommendations(web_html, block_number)
		for n in range(0, len(all_given_rec[0])):
			f.write(str(all_given_rec[0][n].encode('utf-8', 'ignore')) + '\n')
			f.write(str(all_given_rec[1][n].encode('utf-8', 'ignore')) + '\n')
			f.write(str(all_given_rec[2][n].encode('utf-8', 'ignore')) + '\n')
			f.write(str(all_given_rec[3][n].encode('utf-8', 'ignore')) + '\n')
			recommendation_given_text = recommendation_given_text + str(all_given_rec[0][n].encode('utf-8', 'ignore')) + '\n'
			recommendation_given_text = recommendation_given_text + str(all_given_rec[1][n].encode('utf-8', 'ignore')) + '\n'
			recommendation_given_text = recommendation_given_text + str(all_given_rec[2][n].encode('utf-8', 'ignore')) + '\n'
			recommendation_given_text = recommendation_given_text + str(all_given_rec[3][n].encode('utf-8', 'ignore')) + '\n'
			if n < (len(all_given_rec[0]) - 1):
				f.write('+-+-+-+-+-\n')
				recommendation_given_text = recommendation_given_text + '+-+-+-+-+-\n'
		if len(all_given_rec) == 0:
			f.write('NULL\n')
	else:
		f.write('NULLL\n')

	f.write('*'*12 + ' ACCOMPLISHMENTS_LANGUAGE ' + '*'*12 + '\n')
	try:
		buscador.click_that_accomplishment_button(browser, 'accomplishments_expand_languages')
		time.sleep(random.uniform(5.3, 6.7))
		buscador.expand_all(browser)
		web_html = buscador.get_the_soup(browser)
		languages_data = profile_html_handler.get_languages_data(web_html)
	except:
		languages_data = [[],[]]
		f.write('NULL\n')
	
	if languages_data:
		f.write(str(languages_data[0]) + '\n')
	
	f.write('*'*12 + ' ACCOMPLISHMENTS_COURSE ' + '*'*12 + '\n')
	course_text = ''
	try:
		buscador.click_that_accomplishment_button(browser, 'accomplishments_expand_courses')
		time.sleep(random.uniform(5.3, 6.7))
		buscador.expand_all(browser)
		web_html = buscador.get_the_soup(browser)
		courses_data = profile_html_handler.get_course_data(web_html)
	except:
		courses_data = []
		f.write('NULL\n')
		
	if courses_data:
		for i in range(0, len(courses_data[0])):
			course_title = courses_data[0][i].replace('\n', '')
			course_info  = courses_data[1][i].replace('\n', ' ')
			f.write('Title: ' + str(course_title.encode('utf-8', 'ignore')) + '\n')
			f.write('Info: '  + str(course_info.encode('utf-8', 'ignore'))  + '\n')
			course_text = course_text + course_title + '\n'
			course_text = course_text + course_info  + '\n'
			if i < (len(courses_data[0]) - 1):
				f.write('+-+-+-+-+-\n')
				course_text = course_text + '+-+-+-+-+-\n'
	
	#accomplishment_project
	f.write('*'*12 + ' ACCOMPLISHMENTS_PROJECT ' + '*'*12 + '\n')
	projects_text = ''
	try:
		buscador.click_that_accomplishment_button(browser, 'accomplishments_expand_projects')
		time.sleep(random.uniform(5.3, 6.7))
		buscador.expand_all(browser)
		web_html = buscador.get_the_soup(browser)
		projects_data = profile_html_handler.get_projects_data(web_html)
	except:
		projects_data = []
		f.write('NULL\n')
		
	if projects_data:
		for i in range(0, len(projects_data[0])):
			project_title  = projects_data[0][i].replace('\n', '')
			project_resume = projects_data[2][i].replace('\n', ' ')
			f.write('Title: '  + str(project_title.encode('utf-8', 'ignore'))  + '\n')
			f.write('Resume: ' + str(project_resume.encode('utf-8', 'ignore')) + '\n')
			projects_text = projects_text + project_title  + '\n'
			projects_text = projects_text + project_resume + '\n'
			if i < (len(projects_data[0]) - 1):
				f.write('+-+-+-+-+-\n')
				projects_text = projects_text + '+-+-+-+-+-\n'
	
	#accomplishment_certification
	f.write('*'*12 + ' ACCOMPLISHMENTS_CERTIFICATION ' + '*'*12 + '\n')
	certifications_text = ''
	try:
		buscador.click_that_accomplishment_button(browser, 'accomplishments_expand_certifications')
		time.sleep(random.uniform(5.3, 6.7))
		buscador.expand_all(browser)
		web_html = buscador.get_the_soup(browser)
		certifications_data = profile_html_handler.get_certifications_data(web_html)
	except:
		certifications_data = []
		f.write('NULL\n')
		
	if certifications_data:
		for i in range(0, len(certifications_data[0])):
			certificate_title  = certifications_data[0][i].replace('\n', '')
			certificate_entity = certifications_data[2][i].replace('\n', ' ')
			f.write('Title: '    + str(certificate_title.encode('utf-8', 'ignore'))  + '\n')
			f.write('Given by: ' + str(certificate_entity.encode('utf-8', 'ignore')) + '\n')
			certifications_text = certifications_text + certificate_title  + '\n'
			certifications_text = certifications_text + certificate_entity + '\n'
			if i < (len(certifications_data) - 1):
				f.write('+-+-+-+-+-\n')
				certifications_text = certifications_text + '+-+-+-+-+-\n'
	
	#accomplishment_organization 
	f.write('*'*12 + ' ACCOMPLISHMENTS_ORGANIZATION ' + '*'*12 + '\n')
	organizations_text = ''
	try:
		buscador.click_that_accomplishment_button(browser, 'accomplishments_expand_organizations')
		time.sleep(random.uniform(5.3, 6.7))
		buscador.expand_all(browser)
		web_html = buscador.get_the_soup(browser)
		organizations_data = profile_html_handler.get_organizations_data(web_html)
	except:
		organizations_data = []
		f.write('NULL\n')
		
	if organizations_data:
		for i in range(0, len(organizations_data[0])):
			org_name = organizations_data[0][i].replace('\n', '')
			org_pos  = organizations_data[2][i].replace('\n', ' ')
			f.write('Organization: ' + str(org_name.encode('utf-8', 'ignore')) + '\n')
			f.write('Position: '     + str(org_pos.encode('utf-8', 'ignore'))  + '\n')
			organizations_text = organizations_text + org_name + '\n'
			organizations_text = organizations_text + org_pos  + '\n'
			if i < (len(organizations_data) - 1):
				f.write('+-+-+-+-+-\n')
				organizations_text = organizations_text + '+-+-+-+-+-\n'
	
	#accomplishment_honor
	f.write('*'*12 + ' ACCOMPLISHMENTS_HONOR ' + '*'*12 + '\n')
	honors_text = ''
	try:
		buscador.click_that_accomplishment_button(browser, 'accomplishments_expand_honors')
		time.sleep(random.uniform(5.3, 6.7))
		buscador.expand_all(browser)
		web_html = buscador.get_the_soup(browser)
		honors_data = profile_html_handler.get_honors_data(web_html)
	except:
		honors_data = []
		f.write('NULL\n')
		
	if honors_data:
		for i in range(0, len(honors_data[0])):
			honor_title  = honors_data[0][i].replace('\n', '')
			honor_entity = honors_data[2][i].replace('\n', ' ')
			honor_resume = honors_data[3][i].replace('\n', ' ')
			f.write('Title: '    + str(honor_title.encode('utf-8', 'ignore'))  + '\n')
			f.write('Given by: ' + str(honor_entity.encode('utf-8', 'ignore')) + '\n')
			f.write('Resume: '   + str(honor_resume.encode('utf-8', 'ignore')) + '\n')
			honors_text = honors_text + honor_title  + '\n'
			honors_text = honors_text + honor_entity + '\n'
			honors_text = honors_text + honor_resume + '\n'
			if i < (len(honors_data) - 1):
				f.write('+-+-+-+-+-\n')
				honors_text = honors_text + '+-+-+-+-+-\n'
	
	#accomplishment_publication
	f.write('*'*12 + ' ACCOMPLISHMENTS_PUBLICATION ' + '*'*12 + '\n')
	publication_text = ''
	try:
		buscador.click_that_accomplishment_button(browser, 'accomplishments_expand_publications')
		time.sleep(random.uniform(5.3, 6.7))
		buscador.expand_all(browser)
		web_html = buscador.get_the_soup(browser)
		publications_data = profile_html_handler.get_publications_data(web_html)
	except:
		publications_data = []
		f.write('NULL\n')
		
	if publications_data:
		for i in range(0, len(publications_data[0])):
			publication_title   = publications_data[0][i].replace('\n', '')
			publication_journal = publications_data[2][i].replace('\n', ' ')
			publication_resume  = publications_data[3][i].replace('\n', ' ')
			f.write('Title: '   + str(publication_title.encode('utf-8', 'ignore'))   + '\n')
			f.write('Journal: ' + str(publication_journal.encode('utf-8', 'ignore')) + '\n')
			f.write('Resume: '  + str(publication_resume.encode('utf-8', 'ignore'))  + '\n')
			publication_text = publication_text + publication_title   + '\n'
			publication_text = publication_text + publication_journal + '\n'
			publication_text = publication_text + publication_resume  + '\n'
			if i < (len(publications_data) - 1):
				f.write('+-+-+-+-+-\n')
				publication_text = publication_text + '+-+-+-+-+-\n'
	
	#accomplishment_patent
	f.write('*'*12 + ' ACCOMPLISHMENTS_PATENT ' + '*'*12 + '\n')
	patents_text = ''
	try:
		buscador.click_that_accomplishment_button(browser, 'accomplishments_expand_patents')
		time.sleep(random.uniform(5.3, 6.7))
		buscador.expand_all(browser)
		web_html = buscador.get_the_soup(browser)
		patents_data = profile_html_handler.get_patents_data(web_html)
	except:
		patents_data = []
		f.write('NULL\n')
		
	if patents_data:
		for i in range(0, len(patents_data[0])):
			patent_title  = patents_data[0][i].replace('\n', '')
			patent_ref    = patents_data[2][i].replace('\n', ' ')
			patent_resume = patents_data[3][i].replace('\n', ' ')
			f.write('Title: '     + str(patent_title.encode('utf-8', 'ignore'))  + '\n')
			f.write('Reference: ' + str(patent_ref.encode('utf-8', 'ignore'))    + '\n')
			f.write('Resume: '    + str(patent_resume.encode('utf-8', 'ignore')) + '\n')
			patents_text = patents_text + patent_title  + '\n'
			patents_text = patents_text + patent_ref    + '\n'
			patents_text = patents_text + patent_resume + '\n'
			if i < (len(patents_data) - 1):
				f.write('+-+-+-+-+-\n')
				patents_text = patents_text + '+-+-+-+-+-\n'
	
	#accomplishment_scorers
	f.write('*'*12 + ' ACCOMPLISHMENTS_SCORERS ' + '*'*12 + '\n')
	scorers_text = ''
	try:
		buscador.click_that_accomplishment_button(browser, 'accomplishments_expand_test_scores')
		time.sleep(random.uniform(5.3, 6.7))
		buscador.expand_all(browser)
		web_html = buscador.get_the_soup(browser)
		scorers_data = profile_html_handler.get_test_scores_data(web_html)
	except:
		scorers_data = []
		f.write('NULL\n')
		
	if scorers_data:
		for i in range(0, len(scorers_data[0])):
			scorer_title  = scorers_data[0][i].replace('\n', '')
			scorer_score  = scorers_data[2][i].replace('\n', ' ')
			scorer_resume = scorers_data[3][i].replace('\n', ' ')
			f.write('Title: '  + str(scorer_title.encode('utf-8', 'ignore'))  + '\n')
			f.write('Score: '  + str(scorer_score.encode('utf-8', 'ignore'))  + '\n')
			f.write('Resume: ' + str(scorer_resume.encode('utf-8', 'ignore')) + '\n')
			scorers_text = scorers_text + scorer_title  + '\n'
			scorers_text = scorers_text + scorer_score  + '\n'
			scorers_text = scorers_text + scorer_resume + '\n'
			if i < (len(scorers_data) - 1):
				f.write('+-+-+-+-+-\n')
				scorers_text = scorers_text + '+-+-+-+-+-\n'
	
	## Open interests	
	f.write('*'*12 + ' AI_INTERESTS ' + '*'*12 + '\n')
	interests_links = [ url + 'detail/interests/influencers/',
						url + 'detail/interests/companies/',
						url + 'detail/interests/groups/',
						url + 'detail/interests/schools/']
	all_interests = []
	for j in range(0, len(interests_links)):
		browser.get(interests_links[j])
		time.sleep(random.uniform(0.7, 1.1))
		buscador.scroll_interets(browser)
		web_html = buscador.get_the_soup(browser)
		interest_followers = profile_html_handler.get_extra_interests(web_html)
		for i in range(0, len(interest_followers[0])):
			all_interests.append(interest_followers[0][i])
			f.write(str(interest_followers[0][i].encode('utf-8', 'ignore')) + '\n')

	f.write('*'*12 + ' AI_INTERESTS_CURRENT_RELATED ' + '*'*12 + '\n')
	realtes_interests_flag = False
	related_interests = []
	for i in range(0, len(all_interests)):
		if all_interests[i] in current_jobs[1]:
			f.write(str(all_interests[i].encode('utf-8', 'ignore')) + '\n')
			related_interests.append(all_interests[i])
			realtes_interests_flag = True
	if realtes_interests_flag == False:
		f.write('NULL\n')
		
	## Open all activity
	activity_link = url + 'detail/recent-activity/'
	browser.get(activity_link)
	time.sleep(random.uniform(0.3, 0.6))
	buscador.scroll_to_bottom(browser)
	time.sleep(random.uniform(0.2, 0.5))
	buscador.expand_all_activity(browser)
	time.sleep(random.uniform(0.2, 0.5))
	web_html = buscador.get_the_soup(browser)
	
	# all_activity: [0] articles | [1] posts | [2] liked
	
	all_activity = profile_html_handler.get_posts(web_html)
	print 'number articles: ' + str(len(all_activity[0]))
	print 'number posts:    ' + str(len(all_activity[1]))
	print 'number liked:    ' + str(len(all_activity[2]))
	
	f.write('*'*12 + ' ACTIVITY_ARTICLES ' + '*'*12 + '\n')
	activity_articles_text = ''
	if all_activity[0][0] == ['NULL', 'NULL', 'NULL', 'NULL', 'NULL']:
		f.write('NULL\n')
	else:
		for i in range(0, len(all_activity[0])):
			if all_activity[0][i] != ['NULL', 'NULL', 'NULL', 'NULL', 'NULL']:
				f.write(str(all_activity[0][i][0].encode('utf-8', 'ignore')) + '\n')
				f.write(str(all_activity[0][i][1].encode('utf-8', 'ignore')) + '\n')
				f.write(str(all_activity[0][i][2].encode('utf-8', 'ignore')) + '\n')
				f.write(str(all_activity[0][i][3].encode('utf-8', 'ignore')) + '\n')
				f.write(str(all_activity[0][i][4].encode('utf-8', 'ignore')) + '\n')
				activity_articles_text = activity_articles_text + str(all_activity[0][i][0].encode('utf-8', 'ignore')) + '\n'
				activity_articles_text = activity_articles_text + str(all_activity[0][i][1].encode('utf-8', 'ignore')) + '\n'
				activity_articles_text = activity_articles_text + str(all_activity[0][i][2].encode('utf-8', 'ignore')) + '\n'
				activity_articles_text = activity_articles_text + str(all_activity[0][i][3].encode('utf-8', 'ignore')) + '\n'
				activity_articles_text = activity_articles_text + str(all_activity[0][i][4].encode('utf-8', 'ignore')) + '\n'
				if i < (len(all_activity[0]) - 1):
					f.write('+-+-+-+-+-\n')
					activity_articles_text = activity_articles_text + '+-+-+-+-+-\n'
	
	f.write('*'*12 + ' ACTIVITY_POSTS ' + '*'*12 + '\n')
	activity_posts_text = ''
	if all_activity[1][0] == ['NULL', 'NULL', 'NULL', 'NULL', 'NULL']:
		f.write('NULL\n')
	else:
		for i in range(0, len(all_activity[1])):
			if all_activity[1][i] != ['NULL', 'NULL', 'NULL', 'NULL', 'NULL']:
				f.write(str(all_activity[1][i][0].encode('utf-8', 'ignore')) + '\n')
				f.write(str(all_activity[1][i][1].encode('utf-8', 'ignore')) + '\n')
				f.write(str(all_activity[1][i][2].encode('utf-8', 'ignore')) + '\n')
				f.write(str(all_activity[1][i][3].encode('utf-8', 'ignore')) + '\n')
				f.write(str(all_activity[1][i][4].encode('utf-8', 'ignore')) + '\n')
				activity_posts_text = activity_posts_text + str(all_activity[1][i][0].encode('utf-8', 'ignore')) + '\n'
				activity_posts_text = activity_posts_text + str(all_activity[1][i][1].encode('utf-8', 'ignore')) + '\n'
				activity_posts_text = activity_posts_text + str(all_activity[1][i][2].encode('utf-8', 'ignore')) + '\n'
				activity_posts_text = activity_posts_text + str(all_activity[1][i][3].encode('utf-8', 'ignore')) + '\n'
				activity_posts_text = activity_posts_text + str(all_activity[1][i][4].encode('utf-8', 'ignore')) + '\n'
				if i < (len(all_activity[1]) - 1):
					f.write('+-+-+-+-+-\n')
					activity_posts_text = activity_posts_text + '+-+-+-+-+-\n'
					
	f.write('*'*12 + ' ACTIVITY_LIKED ' + '*'*12 + '\n')
	activity_liked_text = ''
	if all_activity[2][0] == ['NULL', 'NULL', 'NULL', 'NULL', 'NULL']:
		f.write('NULL\n')
	else:
		for i in range(0, len(all_activity[2])):
			if all_activity[2][i] != ['NULL', 'NULL', 'NULL', 'NULL', 'NULL']:
				f.write(str(all_activity[2][i][0].encode('utf-8', 'ignore')) + '\n')
				f.write(str(all_activity[2][i][1].encode('utf-8', 'ignore')) + '\n')
				f.write(str(all_activity[2][i][2].encode('utf-8', 'ignore')) + '\n')
				f.write(str(all_activity[2][i][3].encode('utf-8', 'ignore')) + '\n')
				f.write(str(all_activity[2][i][4].encode('utf-8', 'ignore')) + '\n')
				activity_liked_text = activity_liked_text + str(all_activity[2][i][0].encode('utf-8', 'ignore')) + '\n'
				activity_liked_text = activity_liked_text + str(all_activity[2][i][1].encode('utf-8', 'ignore')) + '\n'
				activity_liked_text = activity_liked_text + str(all_activity[2][i][2].encode('utf-8', 'ignore')) + '\n'
				activity_liked_text = activity_liked_text + str(all_activity[2][i][3].encode('utf-8', 'ignore')) + '\n'
				activity_liked_text = activity_liked_text + str(all_activity[2][i][4].encode('utf-8', 'ignore')) + '\n'
				if i < (len(all_activity[2]) - 1):
					f.write('+-+-+-+-+-\n')
					activity_liked_text = activity_liked_text + '+-+-+-+-+-\n'
			
	followers_number = '0'
	f.write('*'*12 + ' ACTIVITY_FOLLOWERS ' + '*'*12 + '\n')
	followers_number = profile_html_handler.get_followers_number(web_html)
	if followers_number:
		f.write(str(followers_number.replace(',', '')) + '\n')
	else:
		f.write('NULL\n')
	
	f.write('*'*12 + ' IS_ACTIVE ' + '*'*12 + '\n')
	f.write('TRUE\n')
	
	f.write('*'*12 + ' CURRENT_POSITION ' + '*'*12 + '\n')
	f.write(str(header_info[2].encode('utf-8', 'ignore')) + '\n')
	
	f.write('*'*12 + ' CURRENT_COMPANY ' + '*'*12 + '\n')
	current_company_head = str(header_info[4].encode('utf-8', 'ignore'))
	f.write(str(header_info[4].encode('utf-8', 'ignore')) + '\n')
	
	f.write('*'*12 + ' MOST_IMPORTANT_CERTIFICATE ' + '*'*12 + '\n')
	matched_titles = job_analyzer.get_titles_from_name(header_info[0])
	if matched_titles:
		for i in range(0, len(matched_titles)):
			f.write(str(matched_titles[i]) + '\n')
	else:
		f.write('NULL\n')
	
	f.write('*'*12 + ' MOST_IMPORTANT_EDUCATION ' + '*'*12 + '\n')
	most_important_education = ''
	if header_info[5]:
		f.write(str(header_info[5].encode('utf-8', 'ignore')) + '\n')
		most_important_education = str(header_info[5].encode('utf-8', 'ignore'))
	else:
		f.write('NULL\n')
	
	f.write('*'*12 + ' FACEBOOK_LINKS ' + '*'*12 + '\n')
	facebook_flag = False
	facebook_link = ''
	for i in range(0, len(other_links)):
		if 'facebook' in other_links[i]:
			facebook_flag = True
			f.write(str(other_links[i].encode('utf-8', 'ignore')) + '\n')
			facebook_link = str(other_links[i].encode('utf-8', 'ignore'))
	if facebook_flag == False:
		f.write('NULL\n')
		
	f.write('*'*12 + ' TWITTER_LINKS ' + '*'*12 + '\n')
	twitter_flag = False
	twitter_link = ''
	for i in range(0, len(other_links)):
		if 'twitter' in other_links[i]:
			twitter_flag = True
			f.write(str(other_links[i].encode('utf-8', 'ignore')) + '\n')
			twitter_link = str(other_links[i].encode('utf-8', 'ignore'))
	if twitter_flag == False:
		f.write('NULL\n')
	
	f.write('*'*12 + ' ALL_LINKS ' + '*'*12 + '\n')
	for i in range(0, len(other_links)):
		f.write(str(other_links[i].encode('utf-8', 'ignore')) + '\n')
	if len(other_links) == 0:
		f.write('NULL\n')
		
	f.write('*'*12 + ' EMAILS ' + '*'*12 + '\n')
	emails_flag = False
	email_adresses = []
	for i in range(0, len(other_links)):
		if 'mailto:' in other_links[i]:
			emails_flag = True
			email = str(other_links[i]).replace('mailto:', '')
			f.write(str(email.encode('utf-8', 'ignore')) + '\n')
			email_adresses.append(str(email.encode('utf-8', 'ignore')))
	if emails_flag == False:
		f.write('NULL\n')
		
	f.close()

	print 'The file ' + str(path) + ' is cooked'
	
	try:
		## Add object to db
		external_employee = ExternalEmployee(url=url,
													name                         = candidate_name,
													type                         = 'External',
													job_title                    = current_jobs,
													job_title_prev               = job_title_prev,
													location                     = location,
													location_prev                = location_prev,
													skills                       = skills,
													ai_endorsements              = ai_endorsements,
													experience                   = exp_int,
													ai_job_started               = ai_job_started,
													ai_current_working_started   = ai_current_working_started,
													ai_previous_working_started  = ai_previous_working_started,
													ai_previous_working_finished = ai_previous_working_finished,
													ai_current_job_title         = ai_current_job_title,
													ai_previous_job_title        = ai_previous_job_title,
													ai_current_company           = ai_current_company,
													ai_previous_company          = ai_previous_company,
													ai_current_locations         = ai_current_locations,
													ai_previoius_locations       = ai_previoius_locations,
													ai_current_working_content   = current_working_content_text,
													ai_previous_working_content  = previous_working_content_text,
													ai_company                   = ai_company,
													ai_interests_current_related = related_interests,
													ai_interests                 = interest_followers[0],
													ai_education                 = interest_followers[1],
													ai_previous_education        = ai_previous_education,
													ai_degree                    = ai_degree,
													ai_previous_degree           = ai_previous_degree,
													ai_education_field           = ai_education_field,
													ai_previous_education_field  = ai_previous_education_field,
													ai_education_start           = ai_education_start,
													ai_education_finished        = ai_education_finished,
													ai_self_intro                = str(ai_self_intro.encode('utf-8', 'ignore')),
													ai_volunteer_experience      = ai_volunteer_experience,
													recommendation_given         = recommendation_given_text,
													recommendation_received      = recommendation_received_text,
													ai_activity_articles         = activity_articles_text,
													ai_activity_posts            = activity_posts_text,
													ai_activity_liked            = activity_liked_text,
													activity_followers           = followers_number.replace(',', ''),
													accomplishment_language      = languages_data[0],
													accomplishment_course        = course_text,
													accomplishment_project       = projects_text,
													accomplishment_certification = certifications_text,
													accomplishment_organization  = organizations_text,
													accomplishment_honor         = honors_text,
													accomplishment_publication   = publication_text,
													accomplishment_patent        = patents_text,
													accomplishment_scorer        = scorers_text,
													is_active                    = 'True',
													currrent_position            = str(header_info[2].encode('utf-8', 'ignore')),
													current_company              = current_company_head,
													most_important_certificate   = matched_titles,
													most_important_education     = most_important_education,
													facebook_link                = facebook_link,
													twitter_link                 = twitter_link,
													emails                       = email_adresses,
													all_links                    = other_links,
													)

		print 'Adding new employee...'
		external_employee.save()
		print 'Employee added to the database'
	except Exception, e:
		print 'Could not add employee to database'
		print(e)
		f_errors.write('Error on the database\n')
		f_errors.write(str(links_pool[i]) + '\n')
		f_errors.write(str(e) + '\n\n')
		pass
	
	return

def analyse(browser, url):
	'''
	Analyses the profile recieved and updates the database.
	
	Parameters
	----------
	browser
				Webdriver element
	url
				String. Linkedin profile url
	
	'''

	
	logging.basicConfig(filename='linkedin_crawler.log', format='%(asctime)s - %(filename)s - %(funcName)s - %(levelname)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)
	logger = logging.getLogger('Linkedin_logger')
	
	link_info = str(url.encode('utf-8', 'ignore'))
	
	logger.info('Analyzing %s', link_info)

	print 'Analyzing: ' + str(url.encode('utf-8', 'ignore'))
	
	accomplishment_buttons_pool = [ 'accomplishments_expand_publications',
									'accomplishments_expand_certifications',
									'accomplishments_expand_honors',
									'accomplishments_expand_languages',
									'accomplishments_expand_organizations',
									'accomplishments_expand_patents',
									'accomplishments_expand_projects',
									'accomplishments_expand_courses',
									'accomplishments_expand_test_scores']
	
	
	# Goes to desired url
	browser.get(url)
	time.sleep(random.uniform(0.7, 1.3))
	# Refresh URL address
	url = browser.current_url
	# Expands top summary if any
	buscador.expand_summary(browser)
	time.sleep(random.uniform(0.3, 0.5))
	# Expands other links (top left)
	buscador.expand_other_links(browser)
	time.sleep(random.uniform(0.5, 0.7))
	# Scrolls to the bottom, so every section is loaded
	buscador.scroll_to_bottom(browser)
	# Expands sections on cv (experience, education...)
	buscador.expand_all(browser)
	time.sleep(random.uniform(0.3, 0.7))
	web_html = buscador.get_the_soup(browser)
	## Get info from profile main page
	# Get info from header
	try:
		header_info    = profile_html_handler.get_top_card(web_html)
		other_links    = profile_html_handler.get_other_links(web_html)
		all_experience = profile_html_handler.get_jobs(web_html)
		all_educations = profile_html_handler.get_education(web_html)
		all_volunteers = profile_html_handler.get_volunteer(web_html)
	except:
		print 'Here is a weird exception'
		debu_file = open('html_code.html', 'w')
		debu_file.write(str(web_html))
		sys.exit()
	previous_jobs  = job_analyzer.filter_jobs(all_experience, 'past_jobs') 
	current_jobs    = job_analyzer.filter_jobs(all_experience, 'current_jobs')
	last_started_job = job_analyzer.most_recent_job(all_experience)
	
	
	## Arranging info for output
	
	candidate_name = header_info[0]
	
	job_title_prev = previous_jobs[0][0]
	
	location = []
	for n in range(0, len(current_jobs[0])):
		if current_jobs[4][n] not in location:
			location.append(current_jobs[4][n])

	for i in range(0, len(previous_jobs[4])):
		last_previous_location = previous_jobs[4][i]
		if last_previous_location != '':
			break
	location_prev = last_previous_location
	
	## Expand Skills
	buscador.expand_skills(browser)
	time.sleep(random.uniform(1.0, 1.3))
	web_html = buscador.get_the_soup(browser)
	skills_endorsements = profile_html_handler.get_skills(web_html)
	skills = skills_endorsements[0]
	
	ai_endorsements = skills_endorsements[1]
	
	experience = job_analyzer.get_experience_years(all_experience)
	exp_int = int(round(experience))
	
	ai_job_started = last_started_job[6]
	
	ai_current_working_started = job_analyzer.get_starting_date(current_jobs, 'job_experience')
	
	ai_previous_working_started = job_analyzer.get_starting_date(previous_jobs, 'job_experience')
	
	ai_previous_working_finished = job_analyzer.get_end_date(previous_jobs, 'job_experience')
	
	ai_current_job_title = []
	ai_current_company = []
	ai_current_locations = []
	ai_current_working_content = []
	for j in range(0, len(current_jobs[0])):
		ai_current_job_title.append(current_jobs[0][j])	
		ai_current_company.append(current_jobs[1][j])
		ai_current_locations.append(current_jobs[4][j])
		ai_current_working_content.append(current_jobs[5][j])
		
	ai_previous_job_title = []
	ai_previous_company = []
	ai_previoius_locations = []
	ai_previous_working_content = []
	for k in range(0 , len(previous_jobs[0])):
		ai_previous_job_title.append(previous_jobs[0][k])
		ai_previous_company.append(previous_jobs[1][k])
		ai_previoius_locations.append(previous_jobs[4][k])
		ai_previous_working_content.append(previous_jobs[5][k])
	
	current_working_content_text = ''
	for i in range(0, len(ai_current_working_content)):
		if ai_current_working_content[i]:
			current_working_content_text = current_working_content_text + str(ai_current_working_content[i].encode('utf-8', 'ignore')) + '\n'
			if i < len(ai_current_working_content):
				current_working_content_text = current_working_content_text + '+-+-+-+-+-\n'
		
	previous_working_content_text = ''
	for i in range(0, len(ai_previous_working_content)):
		if ai_previous_working_content[i]:
			previous_working_content_text = previous_working_content_text + str(ai_previous_working_content[i].encode('utf-8', 'ignore')) + '\n'
			if i < len(ai_previous_working_content):
				previous_working_content_text = previous_working_content_text + '+-+-+-+-+-\n'
	
	ai_company = last_started_job[1]
		
	ai_education = str(all_educations[0][0].encode('utf-8', 'ignore'))
		
	ai_previous_education       = []
	ai_previous_degree          = []
	ai_previous_education_field = []
	for i in range(0, len(all_educations[0])):
		if all_educations[0][i] != '':
			ai_previous_education.append(all_educations[0][i])
		if all_educations[1][i] != '':
			ai_previous_degree.append(all_educations[1][i])
		if all_educations[2][i] != '':
			ai_previous_education_field.append(all_educations[2][i])
	
	ai_degree = str(all_educations[1][0].encode('utf-8', 'ignore'))
	
	ai_education_field = str(all_educations[2][0].encode('utf-8', 'ignore'))
	
	ai_education_start = job_analyzer.get_starting_date(all_educations, 'education')
	
	ai_education_finished = job_analyzer.get_end_date(all_educations, 'education')
	
	ai_self_intro = header_info[8]
	
	ai_volunteer_experience = ''
	for m in range(0, len(all_volunteers[0])):
		ai_volunteer_experience = ai_volunteer_experience + str(all_volunteers[0][m].encode('utf-8', 'ignore')) + '\n'
		ai_volunteer_experience = ai_volunteer_experience + str(all_volunteers[1][m].encode('utf-8', 'ignore')) + '\n'
		ai_volunteer_experience = ai_volunteer_experience + str(all_volunteers[2][m].encode('utf-8', 'ignore')) + '\n'
		ai_volunteer_experience = ai_volunteer_experience + str(all_volunteers[3][m].encode('utf-8', 'ignore')) + '\n'
		ai_volunteer_experience = ai_volunteer_experience + str(all_volunteers[4][m].encode('utf-8', 'ignore')) + '\n'
		ai_volunteer_experience = ai_volunteer_experience + str(all_volunteers[5][m].encode('utf-8', 'ignore')) + '\n'
		ai_volunteer_experience = ai_volunteer_experience + '\n+-+-+-+-+-\n'
		
	## Recommendations block
	recomendation_buttons_names = profile_html_handler.get_recommendation_buttons(web_html)
	received_number = re.findall(r'\d+', str(recomendation_buttons_names[0]))
	given_number    = re.findall(r'\d+', str(recomendation_buttons_names[1]))
	print 'Recieved recss: ' + str(received_number[0])
	print 'Given recsssss: ' + str(given_number[0])
	
	## Open recieved recomendations
	buscador.open_received_recommendations(browser)
	time.sleep(random.uniform(0.2, 0.4))
	web_html = buscador.get_the_soup(browser)
	recommendation_received_text = ''
	if received_number[0] != '0':
		all_received_rec = profile_html_handler.get_recommendations(web_html, 0)
		for n in range(0, len(all_received_rec[0])):
			recommendation_received_text = recommendation_received_text + str(all_received_rec[0][n].encode('utf-8', 'ignore')) + '\n'
			recommendation_received_text = recommendation_received_text + str(all_received_rec[1][n].encode('utf-8', 'ignore')) + '\n'
			recommendation_received_text = recommendation_received_text + str(all_received_rec[2][n].encode('utf-8', 'ignore')) + '\n'
			recommendation_received_text = recommendation_received_text + str(all_received_rec[3][n].encode('utf-8', 'ignore')) + '\n'
			if n < (len(all_received_rec[0]) - 1):
				recommendation_received_text = recommendation_received_text + '+-+-+-+-+-\n'
			
	## Open given recommendations
	buscador.open_given_recommendations(browser)
	time.sleep(random.uniform(0.2, 0.4))
	web_html = buscador.get_the_soup(browser)
	recommendation_given_text = ''
	if given_number[0] != '0':
		if (received_number[0] != '0') and (given_number[0] != '0'):
			block_number = 1
		else:
			block_number = 0
		all_given_rec = profile_html_handler.get_recommendations(web_html, block_number)
		for n in range(0, len(all_given_rec[0])):
			recommendation_given_text = recommendation_given_text + str(all_given_rec[0][n].encode('utf-8', 'ignore')) + '\n'
			recommendation_given_text = recommendation_given_text + str(all_given_rec[1][n].encode('utf-8', 'ignore')) + '\n'
			recommendation_given_text = recommendation_given_text + str(all_given_rec[2][n].encode('utf-8', 'ignore')) + '\n'
			recommendation_given_text = recommendation_given_text + str(all_given_rec[3][n].encode('utf-8', 'ignore')) + '\n'
			if n < (len(all_given_rec[0]) - 1):
				recommendation_given_text = recommendation_given_text + '+-+-+-+-+-\n'

	try:
		buscador.click_that_accomplishment_button(browser, 'accomplishments_expand_languages')
		time.sleep(random.uniform(5.3, 6.7))
		buscador.expand_all(browser)
		web_html = buscador.get_the_soup(browser)
		languages_data = profile_html_handler.get_languages_data(web_html)
	except:
		languages_data = [[],[]]
	
	course_text = ''
	try:
		buscador.click_that_accomplishment_button(browser, 'accomplishments_expand_courses')
		time.sleep(random.uniform(5.3, 6.7))
		buscador.expand_all(browser)
		web_html = buscador.get_the_soup(browser)
		courses_data = profile_html_handler.get_course_data(web_html)
	except:
		courses_data = []
		
	if courses_data:
		for i in range(0, len(courses_data[0])):
			course_title = courses_data[0][i].replace('\n', '')
			course_info  = courses_data[1][i].replace('\n', ' ')
			course_text = course_text + course_title + '\n'
			course_text = course_text + course_info  + '\n'
			if i < (len(courses_data[0]) - 1):
				course_text = course_text + '+-+-+-+-+-\n'
	
	#accomplishment_project
	projects_text = ''
	try:
		buscador.click_that_accomplishment_button(browser, 'accomplishments_expand_projects')
		time.sleep(random.uniform(5.3, 6.7))
		buscador.expand_all(browser)
		web_html = buscador.get_the_soup(browser)
		projects_data = profile_html_handler.get_projects_data(web_html)
	except:
		projects_data = []
		
	if projects_data:
		for i in range(0, len(projects_data[0])):
			project_title  = projects_data[0][i].replace('\n', '')
			project_resume = projects_data[2][i].replace('\n', ' ')
			projects_text = projects_text + project_title  + '\n'
			projects_text = projects_text + project_resume + '\n'
			if i < (len(projects_data[0]) - 1):
				projects_text = projects_text + '+-+-+-+-+-\n'
	
	#accomplishment_certification
	certifications_text = ''
	try:
		buscador.click_that_accomplishment_button(browser, 'accomplishments_expand_certifications')
		time.sleep(random.uniform(5.3, 6.7))
		buscador.expand_all(browser)
		web_html = buscador.get_the_soup(browser)
		certifications_data = profile_html_handler.get_certifications_data(web_html)
	except:
		certifications_data = []
		
	if certifications_data:
		for i in range(0, len(certifications_data[0])):
			certificate_title  = certifications_data[0][i].replace('\n', '')
			certificate_entity = certifications_data[2][i].replace('\n', ' ')
			certifications_text = certifications_text + certificate_title  + '\n'
			certifications_text = certifications_text + certificate_entity + '\n'
			if i < (len(certifications_data) - 1):
				certifications_text = certifications_text + '+-+-+-+-+-\n'
	
	#accomplishment_organization 
	organizations_text = ''
	try:
		buscador.click_that_accomplishment_button(browser, 'accomplishments_expand_organizations')
		time.sleep(random.uniform(5.3, 6.7))
		buscador.expand_all(browser)
		web_html = buscador.get_the_soup(browser)
		organizations_data = profile_html_handler.get_organizations_data(web_html)
	except:
		organizations_data = []
		
	if organizations_data:
		for i in range(0, len(organizations_data[0])):
			org_name = organizations_data[0][i].replace('\n', '')
			org_pos  = organizations_data[2][i].replace('\n', ' ')
			organizations_text = organizations_text + org_name + '\n'
			organizations_text = organizations_text + org_pos  + '\n'
			if i < (len(organizations_data) - 1):
				organizations_text = organizations_text + '+-+-+-+-+-\n'
	
	#accomplishment_honor
	honors_text = ''
	try:
		buscador.click_that_accomplishment_button(browser, 'accomplishments_expand_honors')
		time.sleep(random.uniform(5.3, 6.7))
		buscador.expand_all(browser)
		web_html = buscador.get_the_soup(browser)
		honors_data = profile_html_handler.get_honors_data(web_html)
	except:
		honors_data = []
		
	if honors_data:
		for i in range(0, len(honors_data[0])):
			honor_title  = honors_data[0][i].replace('\n', '')
			honor_entity = honors_data[2][i].replace('\n', ' ')
			honor_resume = honors_data[3][i].replace('\n', ' ')
			honors_text = honors_text + honor_title  + '\n'
			honors_text = honors_text + honor_entity + '\n'
			honors_text = honors_text + honor_resume + '\n'
			if i < (len(honors_data) - 1):
				honors_text = honors_text + '+-+-+-+-+-\n'
	
	#accomplishment_publication
	publication_text = ''
	try:
		buscador.click_that_accomplishment_button(browser, 'accomplishments_expand_publications')
		time.sleep(random.uniform(5.3, 6.7))
		buscador.expand_all(browser)
		web_html = buscador.get_the_soup(browser)
		publications_data = profile_html_handler.get_publications_data(web_html)
	except:
		publications_data = []
		
	if publications_data:
		for i in range(0, len(publications_data[0])):
			publication_title   = publications_data[0][i].replace('\n', '')
			publication_journal = publications_data[2][i].replace('\n', ' ')
			publication_resume  = publications_data[3][i].replace('\n', ' ')
			publication_text = publication_text + publication_title   + '\n'
			publication_text = publication_text + publication_journal + '\n'
			publication_text = publication_text + publication_resume  + '\n'
			if i < (len(publications_data) - 1):
				publication_text = publication_text + '+-+-+-+-+-\n'
	
	#accomplishment_patent
	patents_text = ''
	try:
		buscador.click_that_accomplishment_button(browser, 'accomplishments_expand_patents')
		time.sleep(random.uniform(5.3, 6.7))
		buscador.expand_all(browser)
		web_html = buscador.get_the_soup(browser)
		patents_data = profile_html_handler.get_patents_data(web_html)
	except:
		patents_data = []
		
	if patents_data:
		for i in range(0, len(patents_data[0])):
			patent_title  = patents_data[0][i].replace('\n', '')
			patent_ref    = patents_data[2][i].replace('\n', ' ')
			patent_resume = patents_data[3][i].replace('\n', ' ')
			patents_text = patents_text + patent_title  + '\n'
			patents_text = patents_text + patent_ref    + '\n'
			patents_text = patents_text + patent_resume + '\n'
			if i < (len(patents_data) - 1):
				patents_text = patents_text + '+-+-+-+-+-\n'
	
	#accomplishment_scorers
	scorers_text = ''
	try:
		buscador.click_that_accomplishment_button(browser, 'accomplishments_expand_test_scores')
		time.sleep(random.uniform(5.3, 6.7))
		buscador.expand_all(browser)
		web_html = buscador.get_the_soup(browser)
		scorers_data = profile_html_handler.get_test_scores_data(web_html)
	except:
		scorers_data = []
		
	if scorers_data:
		for i in range(0, len(scorers_data[0])):
			scorer_title  = scorers_data[0][i].replace('\n', '')
			scorer_score  = scorers_data[2][i].replace('\n', ' ')
			scorer_resume = scorers_data[3][i].replace('\n', ' ')
			scorers_text = scorers_text + scorer_title  + '\n'
			scorers_text = scorers_text + scorer_score  + '\n'
			scorers_text = scorers_text + scorer_resume + '\n'
			if i < (len(scorers_data) - 1):
				scorers_text = scorers_text + '+-+-+-+-+-\n'
	
	## Open interests	
	interests_links = [ url + 'detail/interests/influencers/',
						url + 'detail/interests/companies/',
						url + 'detail/interests/groups/',
						url + 'detail/interests/schools/']
	all_interests = []
	for j in range(0, len(interests_links)):
		browser.get(interests_links[j])
		time.sleep(random.uniform(0.7, 1.1))
		buscador.scroll_interets(browser)
		web_html = buscador.get_the_soup(browser)
		interest_followers = profile_html_handler.get_extra_interests(web_html)
		for i in range(0, len(interest_followers[0])):
			all_interests.append(interest_followers[0][i])

	related_interests = []
	for i in range(0, len(all_interests)):
		if all_interests[i] in current_jobs[1]:
			related_interests.append(all_interests[i])
		
	## Open all activity
	activity_link = url + 'detail/recent-activity/'
	browser.get(activity_link)
	time.sleep(random.uniform(0.3, 0.6))
	buscador.scroll_to_bottom(browser)
	time.sleep(random.uniform(0.2, 0.5))
	buscador.expand_all_activity(browser)
	time.sleep(random.uniform(0.2, 0.5))
	web_html = buscador.get_the_soup(browser)
	
	# all_activity: [0] articles | [1] posts | [2] liked
	
	all_activity = profile_html_handler.get_posts(web_html)
	print 'number articles: ' + str(len(all_activity[0]))
	print 'number posts:    ' + str(len(all_activity[1]))
	print 'number liked:    ' + str(len(all_activity[2]))
	
	activity_articles_text = ''
	for i in range(0, len(all_activity[0])):
		if all_activity[0][i] != ['NULL', 'NULL', 'NULL', 'NULL', 'NULL']:
			activity_articles_text = activity_articles_text + str(all_activity[0][i][0].encode('utf-8', 'ignore')) + '\n'
			activity_articles_text = activity_articles_text + str(all_activity[0][i][1].encode('utf-8', 'ignore')) + '\n'
			activity_articles_text = activity_articles_text + str(all_activity[0][i][2].encode('utf-8', 'ignore')) + '\n'
			activity_articles_text = activity_articles_text + str(all_activity[0][i][3].encode('utf-8', 'ignore')) + '\n'
			activity_articles_text = activity_articles_text + str(all_activity[0][i][4].encode('utf-8', 'ignore')) + '\n'
			if i < (len(all_activity[0]) - 1):
				activity_articles_text = activity_articles_text + '+-+-+-+-+-\n'
	
	activity_posts_text = ''
	for i in range(0, len(all_activity[1])):
		if all_activity[1][i] != ['NULL', 'NULL', 'NULL', 'NULL', 'NULL']:
			activity_posts_text = activity_posts_text + str(all_activity[1][i][0].encode('utf-8', 'ignore')) + '\n'
			activity_posts_text = activity_posts_text + str(all_activity[1][i][1].encode('utf-8', 'ignore')) + '\n'
			activity_posts_text = activity_posts_text + str(all_activity[1][i][2].encode('utf-8', 'ignore')) + '\n'
			activity_posts_text = activity_posts_text + str(all_activity[1][i][3].encode('utf-8', 'ignore')) + '\n'
			activity_posts_text = activity_posts_text + str(all_activity[1][i][4].encode('utf-8', 'ignore')) + '\n'
			if i < (len(all_activity[1]) - 1):
				activity_posts_text = activity_posts_text + '+-+-+-+-+-\n'

	activity_liked_text = ''
	for i in range(0, len(all_activity[2])):
		if all_activity[2][i] != ['NULL', 'NULL', 'NULL', 'NULL', 'NULL']:
			activity_liked_text = activity_liked_text + str(all_activity[2][i][0].encode('utf-8', 'ignore')) + '\n'
			activity_liked_text = activity_liked_text + str(all_activity[2][i][1].encode('utf-8', 'ignore')) + '\n'
			activity_liked_text = activity_liked_text + str(all_activity[2][i][2].encode('utf-8', 'ignore')) + '\n'
			activity_liked_text = activity_liked_text + str(all_activity[2][i][3].encode('utf-8', 'ignore')) + '\n'
			activity_liked_text = activity_liked_text + str(all_activity[2][i][4].encode('utf-8', 'ignore')) + '\n'
			if i < (len(all_activity[2]) - 1):
				activity_liked_text = activity_liked_text + '+-+-+-+-+-\n'
	
	followers_number = '0'
	followers_number = profile_html_handler.get_followers_number(web_html)

	current_company_head = str(header_info[4].encode('utf-8', 'ignore'))
	
	matched_titles = job_analyzer.get_titles_from_name(header_info[0])
	
	most_important_education = ''
	if header_info[5]:
		most_important_education = str(header_info[5].encode('utf-8', 'ignore'))
	
	facebook_flag = False
	facebook_link = ''
	for i in range(0, len(other_links)):
		if 'facebook' in other_links[i]:
			facebook_flag = True
			facebook_link = str(other_links[i].encode('utf-8', 'ignore'))
		
	twitter_flag = False
	twitter_link = ''
	for i in range(0, len(other_links)):
		if 'twitter' in other_links[i]:
			twitter_flag = True
			twitter_link = str(other_links[i].encode('utf-8', 'ignore'))
			
	emails_flag = False
	email_adresses = []
	for i in range(0, len(other_links)):
		if 'mailto:' in other_links[i]:
			emails_flag = True
			email = str(other_links[i]).replace('mailto:', '')
			email_adresses.append(str(email.encode('utf-8', 'ignore')))
			
	try:
		## Add object to db
		external_employee = ExternalEmployee(	url                          = url,
												name                         = candidate_name,
												type                         = 'External',
												job_title                    = current_jobs,
												job_title_prev               = job_title_prev,
												location                     = location,
												location_prev                = location_prev,
												skills                       = skills,
												ai_endorsements              = ai_endorsements,
												experience                   = exp_int,
												ai_job_started               = ai_job_started,
												ai_current_working_started   = ai_current_working_started,
												ai_previous_working_started  = ai_previous_working_started,
												ai_previous_working_finished = ai_previous_working_finished,
												ai_current_job_title         = ai_current_job_title,
												ai_previous_job_title        = ai_previous_job_title,
												ai_current_company           = ai_current_company,
												ai_previous_company          = ai_previous_company,
												ai_current_locations         = ai_current_locations,
												ai_previoius_locations       = ai_previoius_locations,
												ai_current_working_content   = current_working_content_text,
												ai_previous_working_content  = previous_working_content_text,
												ai_company                   = ai_company,
												ai_interests_current_related = related_interests,
												ai_interests                 = interest_followers[0],
												ai_education                 = interest_followers[1],
												ai_previous_education        = ai_previous_education,
												ai_degree                    = ai_degree,
												ai_previous_degree           = ai_previous_degree,
												ai_education_field           = ai_education_field,
												ai_previous_education_field  = ai_previous_education_field,
												ai_education_start           = ai_education_start,
												ai_education_finished        = ai_education_finished,
												ai_self_intro                = str(ai_self_intro.encode('utf-8', 'ignore')),
												ai_volunteer_experience      = ai_volunteer_experience,
												recommendation_given         = recommendation_given_text,
												recommendation_received      = recommendation_received_text,
												ai_activity_articles         = activity_articles_text,
												ai_activity_posts            = activity_posts_text,
												ai_activity_liked            = activity_liked_text,
												activity_followers           = followers_number.replace(',', ''),
												accomplishment_language      = languages_data[0],
												accomplishment_course        = course_text,
												accomplishment_project       = projects_text,
												accomplishment_certification = certifications_text,
												accomplishment_organization  = organizations_text,
												accomplishment_honor         = honors_text,
												accomplishment_publication   = publication_text,
												accomplishment_patent        = patents_text,
												accomplishment_scorer        = scorers_text,
												is_active                    = 'True',
												currrent_position            = str(header_info[2].encode('utf-8', 'ignore')),
												current_company              = current_company_head,
												most_important_certificate   = matched_titles,
												most_important_education     = most_important_education,
												facebook_link                = facebook_link,
												twitter_link                 = twitter_link,
												emails                       = email_adresses,
												all_links                    = other_links,
												)
	
		print 'Adding new employee...'
		external_employee.save()
		print 'Employee added to the database'
		logger.info('Succesfully added to database')
	except Exception, e:
		print(e)
		logger.error('Unable to create new database entry')
		logger.error(e)
		pass
		
	return

	
if __name__=="__main__":

	## Create errors file
	cwd = os.getcwd()
	directory = str(cwd) + r'\output_texts\\'
	if not os.path.exists(directory):
		os.makedirs(directory)
	errors_file = directory + r'errors_log.txt'
	f_errors = open(errors_file, 'w')

	
	links_pool = ['https://www.linkedin.com/in/aliciacostalagomeruelo/',
				  'https://www.linkedin.com/in/sinofsky/',
				  'https://www.linkedin.com/in/alicia-hawkins-4740912/',
				  'https://www.linkedin.com/in/jenna-bromberg-1401a0128/',
				  'https://www.linkedin.com/in/tim-foster-b910895/',
				  'https://www.linkedin.com/in/paul-edlund-998479/',
				  'https://www.linkedin.com/in/carl-ross-45a32b32/',
				  'https://www.linkedin.com/in/preethi-kasireddy-41383528/',
				  'https://www.linkedin.com/in/isisanchalee/',
				  'https://www.linkedin.com/in/frankchen/',
				  'https://www.linkedin.com/in/jaimemartinezverdu/',
				  'https://www.linkedin.com/in/danielgoleman/',
				  'https://www.linkedin.com/in/fernando-hernandez-51b1201a/',
				  'https://www.linkedin.com/in/jeffweiner08/',
				  'https://www.linkedin.com/in/timferriss/',
				  'https://www.linkedin.com/in/simonoschneider/',
				  'https://www.linkedin.com/in/ACoAAAjikcwBWTMp7Ai3SJ42ZFPqSghxBwfCDTo/',
				  'https://www.linkedin.com/in/ACoAAAZJgE8BZcjK3Ashscb8hQ6moxuHc1GyTZU/',
				  'https://www.linkedin.com/in/ACoAAAs41QwBOnj4ouhVyvM1DGFBlOXFasEep90/',
				  'https://www.linkedin.com/in/ACoAAAAL4r0BJfkixoD9BeYyvPaddjQBAn_ZZEE/']

	# Opens browser
	browser = buscador.open_browser()
	# Logs in Linkedin
	buscador.logeate(browser)
	time.sleep(random.uniform(0.5, 1.3))

	#analyse(links_pool[0])
	debug_analyse(browser, links_pool[-1])
	
	#for i in range(0, len(links_pool)):
	#	print links_pool[i]
	#	#try:
	#	previous_user = ExternalEmployee.objects.filter(url=links_pool[i])
	#	if not previous_user:
	#		analyse(links_pool[i])
	#	if previous_user:
	#		print str(previous_user[0].name) + 'alredy in the database'
	#		pass
		#except Exception, e:
		#	f_errors.write(str(links_pool[i]) + '\n')
		#	f_errors.write(str(e) + '\n\n')
			
	f_errors.close()