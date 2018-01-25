# -*- coding: UTF-8 -*-

import os
import re
from bs4 import BeautifulSoup

def get_top_card(web_html):
	'''Recieves a LinkedIn profile html and returns a list with the information on the header, just below the name title.
	
	Parameters
	----------
	web_html
				Html code of a LinkedIn profile.
				
	Returns
	-------
	list
			[0] : Name
			[1] : Distance on network
			[2] : Current position
			[3] : Current company
			[4] : Last company
			[5] : Last education
			[6] : Location
			[7] : Number of connections_html
			[8] : Summary
	'''	

	
	info_block = []

	#top_card_section = web_html.find('div', attrs={'class':'pv-top-card-section__information mt3 ember-view'})
	top_card_section = web_html.find('section', attrs={'class':'pv-profile-section pv-top-card-section artdeco-container-card ember-view'})

	# Get the name
	name_html = top_card_section.find('h1', attrs={'class':'pv-top-card-section__name Sans-26px-black-85%'})
	name_html = web_html.find('h1', attrs={'class':'pv-top-card-section__name Sans-26px-black-85%'})
	if name_html:
		name_text = name_html.text.strip()
	if not name_html:
		name_text = ''
		print ('ERROR: No name_section not found')
		print ('Other labels found:')
		all_classes = top_card_section.find_all('h1')
		for i in range(0, len(all_classes)):
			try:
				print ('\t' + str(all_classes[i]['class']))
			except:
				pass
	#print 'Name: ' + str(name_text.encode('utf-8'))

	# Get distance value (network distance)
	distance_html = top_card_section.find('span', attrs={'class':'dist-value'})
	if distance_html:
		distance_text = distance_html.text.strip()
		if not distance_text:
			distance_text = 'Not in network'
	#print 'Distance: ' + str(distance_text)

	# Get current employment line, just below the name
	current_ocupation_html = top_card_section.find('h2', attrs={'class':'pv-top-card-section__headline Sans-19px-black-85%'})
	if current_ocupation_html:
		current_ocupation_text = current_ocupation_html.text.strip()
		current_broken = current_ocupation_text.split(' at ')
		current_position = current_broken[0]
		if len(current_broken) > 1:
			current_company  = current_broken[1]
		if len(current_broken) == 1:
			current_company = ''
	if not current_ocupation_html:
		current_position = ''
		current_company  = ''
	#print 'Current postion: ' + str(current_position.encode('utf-8'))
	#print 'Current company: ' + str(current_company.encode('utf-8'))

	# Get last company
	last_company_html = top_card_section.find('h3', attrs={'class':'pv-top-card-section__company Sans-17px-black-70% mb1 inline-block'})
	if last_company_html:
		last_company_text = last_company_html.text.strip()
	if not last_company_html:
		last_company_text = ''
	#print 'Last company: ' + str(last_company_text.encode('utf-8'))

	# Get last education
	last_education_html = top_card_section.find('h3', attrs={'class':'pv-top-card-section__school pv-top-card-section__school--with-separator Sans-17px-black-70% mb1 inline-block'})
	if last_education_html:
		last_education_text = last_education_html.text.strip()
	if not last_education_html:
		last_education_text = ''
	#print 'Last education: ' + str(last_education_text.encode('utf-8'))
	
	# Get current location
	location_html = top_card_section.find('h3', attrs={'class':'pv-top-card-section__location Sans-17px-black-70% mb1 inline-block'})
	if location_html:
		location_text = location_html.text.strip()
	if not location_html:
		location_text = ''
	#print 'Location: ' + str(location_text.encode('utf-8'))
	
	# Get number of conections
	connections_text = ''
	connections_html = top_card_section.find('h3', attrs={'class':'pv-top-card-section__connections pv-top-card-section__connections--with-separator Sans-17px-black-70% mb1 inline-block'})
	if connections_html:
		connections_span = connections_html.find('span')
		if connections_span:
			connections_text = connections_span.text.strip()
	#print 'Connections: ' + str(connections_text)
	
	# Get summary_html
	summary_html = web_html.find('p', attrs={'class':'pv-top-card-section__summary-text text-align-left Sans-15px-black-55% mt5 pt5 ember-view'})
	if summary_html:
		summary_text = summary_html.text.strip()
	if not summary_html:
		summary_text = ''
	#print summary_text.encode('utf-8')
	
	info_block.append(name_text)
	info_block.append(distance_text)
	info_block.append(current_position)
	info_block.append(current_company)
	info_block.append(last_company_text)
	info_block.append(last_education_text)
	info_block.append(location_text)
	info_block.append(connections_text)
	info_block.append(summary_text)
	
	return info_block

def get_other_links(web_html):
	'''Recieves a LinkedIn profile html and returns a list with the links on the contact personal information.
	
	Parameters
	----------
	web_html
				Html code of the web to be analysed
				
	Returns
	-------
	list
			Conains all the links shown in the contact personal information
	'''	

	links_pool = []
	
	contact_info_block = web_html.find('section', attrs={'class':'pv-profile-section pv-contact-info artdeco-container-card ember-view'})
	
	if contact_info_block:
		for link in contact_info_block.find_all('a', href=True):
			links_pool.append(link['href'])
	
	if not contact_info_block:
		print ('ERROR: No other links section found')
		print ('Other sections found:')
		all_secs = web_html.fin_all('section')
		for i in range(0, len(all_secs)):
			try:
				print ('\t' + str(all_secs[i]['class']))
			except:
				pass
	
	return links_pool
	
def get_jobs(web_html):
	'''Recieves a LinkedIn profile html and returns a list with the information displayed on the experience section.
	
	Parameters
	----------
	web_html
				Html code of a LinkedIn profile.
				
	Returns
	-------
	list
			[0] : Companies at which the candidate has work
			[1] : Dates, start and end time of the position
			[2] : Time spent at the position
			[3] : Locations at which the position was developed
			[4] : Resumes of the positions
	'''	


	all_experience = []
	positions = []
	companies = []
	dates = []
	time_spent = []
	locations = []
	resumes = []
	
	ul_class_pool = ['pv-profile-section__section-info section-info pv-profile-section__section-info--has-more',
					 'pv-profile-section__section-info section-info pv-profile-section__section-info--has-more ember-view',
					 'pv-profile-section__section-info section-info pv-profile-section__section-info--has-no-more',
					 'pv-profile-section__section-info section-info pv-profile-section__section-info--has-no-more ember-view',]


	experience_section = web_html.find('section', attrs={'class':'pv-profile-section experience-section ember-view'})
	
	if experience_section:
	
		for i in range(0, len(ul_class_pool)):
			experience_block = experience_section.find('ul', attrs={'class':ul_class_pool})
			if experience_block:
				break

		if not experience_block:		
			print ('ERROR: No experience_block found.')
			print ('Others uls found:')
			all_uls = experience_section.find_all('ul')
			for i in range(0, len(all_uls)):
				try:
					print ('\t' + str(all_uls[i]['class']))
				except:
					pass
	
		for child in experience_block.children:
			if len(child) > 1:
				# Create html item
				job = BeautifulSoup(str(child), 'html.parser')
				# Get position
				position_html = job.find('h3')
				if position_html:
					position_text = position_html.text.strip()
					positions.append(position_text)
				if not position_html:
					positions.append('')
				# Get company
				company_html = job.find('h4', attrs={'class':'Sans-17px-black-85%'})
				if company_html:
					company_text = company_html.text.strip()
					companies.append(company_text.replace('Company Name\n', ''))
				if not company_html:
					companies.append('')
				# Get dates
				date_html = job.find('h4', attrs={'class':'pv-entity__date-range inline-block Sans-15px-black-70%'})
				if date_html:
					date_text = date_html.text.strip()
					dates.append(date_text.replace('Dates Employed\n', ''))
				if not date_html:
					dates.append('')
				# Get time spent
				time_html = job.find('h4', attrs={'class':'inline-block Sans-15px-black-70%'})
				if time_html:
					time_text = time_html.text.strip()
					time_spent.append(time_text.replace('Employment Duration\n', ''))
				if not time_html:
					time_spent.append('')
				# Get location
				loc_html = job.find('h4', attrs={'class':'pv-entity__location Sans-15px-black-70% block'})
				if loc_html:
					loc_text = loc_html.text.strip()
					locations.append(loc_text.replace('Location\n', ''))
				if not loc_html:
					locations.append('')
				# Get resume
				resume_html = job.find('div', attrs={'class':'pv-entity__extra-details'})
				if resume_html:
					resume_text = resume_html.text.strip()
					resumes.append(resume_text)
				if not resume_html:
					resumes.append('')
	
				all_experience.append(positions)
				all_experience.append(companies)
				all_experience.append(dates)
				all_experience.append(time_spent)
				all_experience.append(locations)
				all_experience.append(resumes)
	
	if not experience_section:
		all_experience.append(positions)
		all_experience.append(companies)
		all_experience.append(dates)
		all_experience.append(time_spent)
		all_experience.append(locations)
		all_experience.append(resumes)
	return all_experience
	
def get_education(web_html):
	'''Recieves a LinkedIn profile html and returns a list with the information displayed on the education section.
	
	Parameters
	----------
	web_html
				Html code of a LinkedIn profile.
				
	Returns
	-------
	list
			[0] : Institutions at which the studies have been developed
			[1] : Degrees title
			[2] : Fields of study
			[3] : Dates of studies
			[4] : Others. Other information displayed
			[5] : Resumes. Information about the education
	'''	
	

	all_educations = []
	institutions = []
	degrees = []
	fields = []
	dates = []
	others = []
	resumes = []
	
	ul_class_pool = ['pv-profile-section__section-info section-info pv-profile-section__section-info--has-more',
					 'pv-profile-section__section-info section-info pv-profile-section__section-info--has-more ember-view',
					 'pv-profile-section__section-info section-info pv-profile-section__section-info--has-no-more',
					 'pv-profile-section__section-info section-info pv-profile-section__section-info--has-no-more ember-view',]

	
	education_section = web_html.find('section', attrs={'class':'pv-profile-section education-section ember-view'})
	
	if education_section:
	
		for i in range(0, len(ul_class_pool)):
			education_block = education_section.find('ul', attrs={'class':ul_class_pool})
			if education_block:
				break
				
		if not education_block:
			print ('ERROR: no education_block found')
			print ('Others uls found:')
			all_uls = education_section.find_all('ul')
			for i in range(0, len(all_uls)):
				try:
					print ('\t' + str(all_uls[i]['class']))
				except:
					pass
		
		if education_block:
			for child in education_block.children:
				if len(child) > 1:
					# Generate html item
					edu = BeautifulSoup(str(child), 'html.parser')
					# Get the school or institution
					institution = edu.find('h3')
					if institution:
						institution_text = institution.text.strip()
						institutions.append(institution_text)
						#print institution_text
					if not institution:
						institutions.append('')
					# Get the 
					degree = edu.find('p', attrs={'class':'pv-entity__secondary-title pv-entity__degree-name pv-entity__secondary-title Sans-15px-black-85%'})
					if degree:
						degree_text = degree.text.strip()
						degrees.append(degree_text.replace('Degree Name\n', ''))
						#print degree_text.replace('Degree Name\n', '')
					if not degree:
						degrees.append('')
					# Get the field
					field = edu.find('p', attrs={'class':'pv-entity__secondary-title pv-entity__fos pv-entity__secondary-title Sans-15px-black-70%'})
					if field:
						field_text = field.text.strip()
						#print field_text.replace('Field Of Study\n', '')
						fields.append(field_text.replace('Field Of Study\n', ''))
					if not field:
						fields.append('')
					# Get the dates
					date = edu.find('p', attrs={'class':'pv-entity__dates Sans-15px-black-70%'})
					if date:
						date_text = date.text.strip()
						#print date_text.replace('Dates attended or expected graduation\n\n', '')
						dates.append(date_text.replace('Dates attended or expected graduation\n\n', ''))
					if not date:
						dates.append('')
					# Get others, such as activites and societies...
					other = edu.find('p', attrs={'class':'pv-entity__secondary-title Sans-15px-black-70%'})
					if other:
						other_text = other.text.strip()
						#print other_text.replace('Activities and Societies:\n', '')
						others.append(other_text.replace('Activities and Societies:\n', ''))
					if not other:
						others.append('')
					# Get the resumes
					resume = edu.find('div', attrs={'class':'pv-entity__extra-details'})
					if resume:
						resume_text = resume.text.strip()
						#print resume_text
						resumes.append(resume_text)
					if not resume:
						resumes.append('')
					#print ''
			
				all_educations.append(institutions)
				all_educations.append(degrees)
				all_educations.append(fields)
				all_educations.append(dates)
				all_educations.append(others)
				all_educations.append(resumes)
				
	if not education_section:
		institutions.append('NULL')
		degrees.append('NULL')
		fields.append('NULL')
		dates.append('NULL')
		others.append('NULL')
		resumes.append('NULL')
	
		all_educations.append(institutions)
		all_educations.append(degrees)
		all_educations.append(fields)
		all_educations.append(dates)
		all_educations.append(others)
		all_educations.append(resumes)
	return all_educations

def get_volunteer(web_html):
	'''Recieves a LinkedIn profile html and returns a list with the information displayed on the volunteer section.
	
	Parameters
	----------
	web_html
				Html code of a LinkedIn profile.
				
	Returns
	-------
	list
			[0] : Position titles
			[1] : Companies or organizations
			[2] : Dates of start and end
			[3] : Total time spent at each position
			[4] : Others. Other information displayed
			[5] : Resumes. Information about the volunteer
	'''		
	

	titles         = []
	companies      = []
	dates          = []
	times          = []
	others         = []
	resumes        = []
	all_volunteers = []	
	
	ul_class_pool = ['pv-profile-section__section-info section-info pv-profile-section__section-info--has-more',
					 'pv-profile-section__section-info section-info pv-profile-section__section-info--has-more ember-view',
					 'pv-profile-section__section-info section-info pv-profile-section__section-info--has-no-more',
					 'pv-profile-section__section-info section-info pv-profile-section__section-info--has-no-more ember-view',]

	volunteer_section = web_html.find('section', attrs={'class':'pv-profile-section volunteering-section ember-view'})	
	
	volunteer_flag = True
	
	if volunteer_section:
		for i in range(0, len(ul_class_pool)):
			volunteer_block = volunteer_section.find('ul', attrs={'class':ul_class_pool})
			if volunteer_block:
				break
	
		if not volunteer_block:
			print ('ERROR: No volunteer_block found.')
			print ('Other uls found:')
			all_uls = volunteer_section.fin_all('ul')
			for i in range(0, len(all_uls)):
				try:
					print ('\t' + str(all_uls[i]['class']))
				except:
					pass
	
		if volunteer_block:
			for child in volunteer_block.children:
				if len(child) > 1:
					# Generate html item
					volunteer = BeautifulSoup(str(child), 'html.parser')
					# Get title
					title_html = volunteer.find('h3', attrs={'class':'Sans-17px-black-85%-semibold'})
					if title_html:
						title_text = title_html.text.strip()
					if not title_html:
						title_text = ''
					#print title_text.encode('utf-8')
					titles.append(title_text)
					# Get company
					company_html = volunteer.find('h4', attrs={'class':'Sans-15px-black-85%'})
					if company_html:
						company_text = company_html.text.strip()
					if not company_html:
						company_text = ''
					#print company_text.encode('utf-8')
					companies.append(company_text.replace('Company Name\n', ''))
					# Get dates
					date_html = volunteer.find('h4', attrs={'class':'pv-entity__date-range detail-facet inline-block Sans-15px-black-70%'})
					if date_html:
						date_text = date_html.text.strip()
					if not date_html:
						date_text = ''
					#print date_text.encode('utf-8')
					dates.append(date_text.replace('Dates volunteered\n', ''))
					# Get time
					time_html = volunteer.find('h4', attrs={'class':'detail-facet inline-block Sans-15px-black-70%'})
					if time_html:
						time_text = time_html.text.strip()
					if not time_html:
						time_text = ''
					#print time_text.encode('utf-8')
					times.append(time_text.replace('Volunteer duration\n', ''))
					# Get others
					others_html = volunteer.find('h4', attrs={'class':'pv-entity__cause Sans-15px-black-70%'})
					if others_html:
						other_text = others_html.text.strip()
					if not others_html:
						other_text = ''
					#print other_text.encode('utf-8')
					others.append(other_text.replace('Cause', ''))
					# Get resume
					resume_html = volunteer.find('div', attrs={'class':'pv-entity__extra-details'})
					if resume_html:
						resume_text = resume_html.text.strip()
					if not resume_html:
						resume_text = ''
					#print resume_text.encode('utf-8')
					resumes.append(resume_text)
		
				all_volunteers.append(titles)
				all_volunteers.append(companies)
				all_volunteers.append(dates)
				all_volunteers.append(times)
				all_volunteers.append(others)
				all_volunteers.append(resumes)
				
	if not volunteer_section:
		all_volunteers.append(titles)
		all_volunteers.append(companies)
		all_volunteers.append(dates)
		all_volunteers.append(times)
		all_volunteers.append(others)
		all_volunteers.append(resumes)
		
	return all_volunteers

def get_skills(web_html):
	'''Recieves a LinkedIn profile html and returns a list with the information displayed on the skills section.
	
	Parameters
	----------
	web_html
				Html code of a LinkedIn profile.
				
	Returns
	-------
	list
			[0] : Skill names
			[1] : Skill number of endorsements
	'''	


	name_number = []
	skill_names = []
	skill_endorsmentes = []
	
	class_labels = ['pv-profile-section pv-featured-skills-section artdeco-container-card ember-view',
					'pv-profile-section pv-featured-skills-section artdeco-container-card first-degree ember-view']

	# Find section
	for i in range(0, len(class_labels)):
		skills_section = web_html.find('section', attrs={'class':class_labels[i]})
		if skills_section:
			break	
		
	if skills_section:	
		# Get top list
		top_list = skills_section.find_all('li', attrs={'class':'pv-skill-entity--featured pb5 pv-skill-entity relative pv-skill-entity--include-highlights ember-view'})
		for item in top_list:
			spans_list = item.find_all('span')
			skill_name = spans_list[0].text.strip()
			skill_names.append(skill_name)
			if len(spans_list) > 1:
				endorsments = spans_list[1].text.strip()
				no_see = endorsments.replace('See ', '')
				no_endors = no_see.replace(' endorsements for ', '')
				no_endor = no_endors.replace(' endorsement for ', '')
				no_name = no_endor.replace(skill_name, '')
				try:
					number_integer = int(no_name)
				except:
					no_name = '0'
			else:
				no_name = '0'
			skill_endorsmentes.append(no_name)
		# Get pool list
		pool_list = skills_section.find_all('li', attrs={'class':'pv-skill-entity--featured pb5 pv-skill-entity relative ember-view'})
		if pool_list:
			for item in pool_list:
				spans_list = item.find_all('span')
				skill_name = spans_list[0].text.strip()
				skill_names.append(skill_name)
				if len(spans_list) > 1:
					endorsments = spans_list[1].text.strip()
					no_see = endorsments.replace('See ', '')
					no_endors = no_see.replace(' endorsements for ', '')
					no_endor = no_endors.replace(' endorsement for ', '')
					no_name = no_endor.replace(skill_name, '')
					try:
						number_integer = int(no_name)
					except:
						no_name = '0'
				else:
					no_name = '0'
				skill_endorsmentes.append(no_name)
	
	name_number.append(skill_names)
	name_number.append(skill_endorsmentes)
	return name_number

def get_recommendation_buttons(web_html):
	'''Not in use.
	Gets the text on the recommendation labels.'''
	#html/body/div[5]/div[4]/div[2]/div/div/div/div[2]/div[1]/div[2]/div[6]/div/section/div/artdeco-tabs/artdeco-tablist/artdeco-tab[1]
	#html/body/div[5]/div[4]/div[2]/div/div/div/div[2]/div[1]/div[2]/div[6]/div/section/div/artdeco-tabs/artdeco-tablist/artdeco-tab[2]

	received_text = ''
	given_text    = ''
	recommendation_text = []
	
	
	received_number = re.findall('Received \([0-9]+\)', str(web_html))
	if received_number:
		received_text = received_number[0]
	given_number = re.findall('Given \([0-9]+\)', str(web_html))
	if given_number:
		given_text = given_number[0]
		
	recommendation_text.append(received_text)
	recommendation_text.append(given_text)

	return recommendation_text
	
def get_recieved_recommendations(web_html):
	'''Recieves a LinkedIn profile html and returns a list with the recieved recommendations information.
	
	Parameters
	----------
	web_html
				Html code of a LinkedIn profile.
				
	Returns
	-------
	list
			[0] : Name of the person to whom the recommendation was written
			[1] : Recommendees positions
			[2] : Professional relationship with the candidate
			[3] : Recommendation text
	'''
	

	person_names       = []
	person_titles      = []
	common_works       = []
	recommendations    = []
	all_recomentadions = []
	
	recommendations_html = web_html.find('artdeco-tabs', attrs={'class':'ivy-tabs ember-view'})
	if recommendations_html:
		recommendations_block = recommendations_html.find('ul', attrs={'class':'section-info'})

	if recommendations_block:
		for child in recommendations_block.children:
			if len(child) > 1:
				item = BeautifulSoup(str(child), 'html.parser')
				# Get name of person who gives the recommendation
				person_html = item.find('h3', attrs={'class':'Sans-17px-black-85%-semibold-dense'})
				if person_html:
					person_text = person_html.text.strip()
				if not person_html:
					person_text = ''
				#print 'Recommendation given by: ' + str(person_text.encode('utf-8'))
				person_names.append(person_text)
				# Get the title of the person who gives the recommendation
				person_title_html = item.find('p', attrs={'class':'pv-recommendation-entity__headline Sans-15px-black-55% pb1'})
				if person_title_html:
					person_title_text = person_title_html.text.strip()
				if not person_title_html:
					person_title_text = ''
				#print 'Title: ' + str(person_title_text.encode('utf-8'))
				person_titles.append(person_title_text)
				# Get the time and the company where they work together
				common_html = item.find('p', attrs={'class':'Sans-13px-black-55%'})
				if common_html:
					common_text = common_html.text.strip()
				if not common_html:
					common_text = ''
				#print 'Work together: ' + str(common_text.encode('utf-8'))
				common_works.append(common_text)
				# Get the recommendation text
				recommendation_html = item.find('div', attrs={'class':'pv-recommendation-entity__highlights'})
				if recommendation_html:
					recommendation_text = recommendation_html.text.strip()
				if not recommendation_html:
					recommendation_text = ''
				#print 'Recommendation: ' + str(recommendation_text.encode('utf-8'))
				recommendations.append(recommendation_text)
	
				all_recomentadions.append(person_names)
				all_recomentadions.append(person_titles)
				all_recomentadions.append(common_works)
				all_recomentadions.append(recommendations)
		
	return all_recomentadions
	
	
def get_given_recommendations(web_html):
	'''Recieves a LinkedIn profile html and returns a list with the given recommendations information.
	
	Parameters
	----------
	web_html
				Html code of a LinkedIn profile.
				
	Returns
	-------
	list
			[0] : Name of the person to whom the recommendation was written
			[1] : Recommendees positions
			[2] : Professional relationship with the candidate
			[3] : Recommendation text
	'''


	person_names       = []
	person_titles      = []
	common_works       = []
	recommendations    = []
	all_recomentadions = []
	
	recommendations_html = web_html.find('artdeco-tabs', attrs={'class':'ivy-tabs ember-view'})
	if recommendations_html:
		recommendations_block = recommendations_html.find_all('ul', attrs={'id':'recommendation-list'})
		
	if not recommendations_block[1]:
		print ('ERROR: no recommendations_block[1] found.')
		print ('Other uls found:')
		for i in range(0, len(recommendations_block)):
			print ('\t' + str(recommendations_block[i]))
		
	if recommendations_block[1]:
		for child in recommendations_block[1].children:
			if len(child) > 1:
				# Create html item
				item = BeautifulSoup(str(child), 'html.parser')
				# Get the name
				name_html = item.find('h3', attrs={'class':'Sans-17px-black-85%-semibold-dense'})
				if name_html:
					name_text = name_html.text.strip()
				else:
					name_text = 'NULL'
				person_names.append(name_text)
				# Get position
				position_html = item.find('p', attrs={'class':'pv-recommendation-entity__headline Sans-15px-black-55% pb1'})
				if position_html:
					position_text = position_html.text.strip()
				else:
					position_text = 'NULL'
				person_titles.append(position_text)
				# Get common works
				common_works_html= item.find('p', attrs={'class':'Sans-13px-black-55%'})
				if common_works_html:
					common_works_text = common_works_html.text.strip()
				else:
					common_works_text = 'NULL'
				common_works.append(common_works_text)
				# Get recommendation text
				recommendation_html = item.find('div', attrs={'class':'pv-recommendation-entity__highlights'})
				if recommendation_html:
					recommendation_text = recommendation_html.text.strip()
				else:
					recommendation_text = 'NULL'
				recommendations.append(recommendation_text)
				
				all_recomentadions.append(person_names)
				all_recomentadions.append(person_titles)
				all_recomentadions.append(common_works)
				all_recomentadions.append(recommendations)
	
	return all_recomentadions

def get_recommendations(web_html, block_number):

	## Check this docs
	
	'''Recieves a LinkedIn profile html and returns a list with the given recommendations information.
	
	Parameters
	----------
	web_html
				Html code of a LinkedIn profile.
	
	block_number
				
				
	Returns
	-------
	list
			[0] : Name of the person to whom the recommendation was written
			[1] : Recommendees positions
			[2] : Professional relationship with the candidate
			[3] : Recommendation text
	'''


	person_names       = []
	person_titles      = []
	common_works       = []
	recommendations    = []
	all_recomentadions = []
	
	recommendations_html = web_html.find('artdeco-tabs', attrs={'class':'ivy-tabs ember-view'})
	if recommendations_html:
		recommendations_block = recommendations_html.find_all('ul', attrs={'id':'recommendation-list'})
		
		if not recommendations_block[block_number]:
			print ('ERROR: recommendations_block[' + str(block_number) + '] not found.')
			print ('Other uls found:')
			for i in range(0, len(recommendations_block)):
				try:
					print ('\t' + str(recommendations_block[i]['id']))
				except:
					pass
		
	if recommendations_block[block_number]:
		for child in recommendations_block[block_number].children:
			if len(child) > 1:
				# Create html item
				item = BeautifulSoup(str(child), 'html.parser')
				# Get the name
				name_html = item.find('h3', attrs={'class':'Sans-17px-black-85%-semibold-dense'})
				if name_html:
					name_text = name_html.text.strip()
				else:
					name_text = 'NULL'
				person_names.append(name_text)
				# Get position
				position_html = item.find('p', attrs={'class':'pv-recommendation-entity__headline Sans-15px-black-55% pb1'})
				if position_html:
					position_text = position_html.text.strip()
				else:
					position_text = 'NULL'
				person_titles.append(position_text)
				# Get common works
				common_works_html= item.find('p', attrs={'class':'Sans-13px-black-55%'})
				if common_works_html:
					common_works_text = common_works_html.text.strip()
				else:
					common_works_text = 'NULL'
				common_works.append(common_works_text)
				# Get recommendation text
				recommendation_html = item.find('div', attrs={'class':'pv-recommendation-entity__highlights'})
				if recommendation_html:
					recommendation_text = recommendation_html.text.strip()
				else:
					recommendation_text = 'NULL'
				recommendations.append(recommendation_text)
				
				all_recomentadions.append(person_names)
				all_recomentadions.append(person_titles)
				all_recomentadions.append(common_works)
				all_recomentadions.append(recommendations)
	
	return all_recomentadions

	
def get_accomplishment_button_names(web_html):
	'''Recieves a LinkedIn profile html and returns a list with the class name labels of the accomplishments section.
	
	Parameters
	----------
	web_html
				Html code of a LinkedIn profile.
				
	Returns
	-------
	list
			Class labels of the accomplishmet blocks

	'''

	
	buttons_list = []
	accomplishment_block = web_html.findAll('button', attrs={'class':'pv-accomplishments-block__expand'})
	for i in range(0, len(accomplishment_block)):
		button_attribute = accomplishment_block[i]['data-control-name']
		if button_attribute not in buttons_list:
			buttons_list.append(button_attribute)
	return buttons_list

def get_publications_data(web_html):
	'''Recieves a LinkedIn profile html and returns a list with the publications information.
	
	Parameters
	----------
	web_html
				Html code of a LinkedIn profile.
				
	Returns
	-------
	list
			[0] : Publication titles
			[1] : Dates of publications
			[2] : Journals in which are publish the publications
			[3] : Resumes of publications
			[4] : Links of publications
	'''


	titles_pool       = [] 
	dates_pool        = []
	journals_pool     = []
	resumes_pool      = []
	links_pool        = []
	publications_data = []
	
	class_labels = ['pv-accomplishments-block__list ',
					'pv-accomplishments-block__list pv-accomplishments-block__list--has-more']
	
	publications_block = web_html.find('section', attrs={'class':'accordion-panel pv-profile-section pv-accomplishments-block publications pv-accomplishments-block--expanded ember-view'})
	
	for i in range(0, len(class_labels)):
		publications_list  = publications_block.find('ul', attrs={'class':class_labels[i]})
		if publications_list:
			break
	
	if not publications_list:
		print ('ERROR: publications_list not found.')
		print ('Other uls found:')
		all_uls = publications_block.find_all('ul')
		for i in range(0, len(all_uls)):
			try:
				print ('\t' + str(all_uls[i]['class']))
			except:
				pass
	
	for child in publications_list.children:
		if len(child) > 1:
			item = BeautifulSoup(str(child), "html.parser")
		
			# Get publication title
			#title_html = publis_block[n].find('h4', attrs={'class':'pv-accomplishment-entity__title'})
			title_html = item.find('h4', attrs={'class':'pv-accomplishment-entity__title'})
			title_text = ''
			if title_html:
				title_text = title_html.text.strip()
			titles_pool.append(title_text.replace('publication title\n', ''))
			#print 'Title: ' + str(title_text.encode('utf-8'))
			# Get publication date
			#date_html = publis_block[n].find('span', attrs={'class':'pv-accomplishment-entity__date'})
			date_html = item.find('span', attrs={'class':'pv-accomplishment-entity__date'})
			date_text = ''
			if date_html:
				date_text = date_html.text.strip()
			dates_pool.append(date_text.replace('publication date', ''))
			#print 'Date: ' + str(date_text.encode('utf-8'))
			# Get publcation journal
			#journal_html = publis_block[n].find('span', attrs={'class':'pv-accomplishment-entity__publisher'})
			journal_html = item.find('span', attrs={'class':'pv-accomplishment-entity__publisher'})
			journal_text = ''
			if journal_html:
				journal_text = journal_html.text.strip()
			journals_pool.append(journal_text.replace('publication description\n', ''))
			#print 'Journal: ' + str(journal_text.encode('utf-8'))
			# Get publication resume
			#resume_html = publis_block[n].find('p', attrs={'class':'pv-accomplishment-entity__description Sans-15px-black-70%'})
			resume_html = item.find('p', attrs={'class':'pv-accomplishment-entity__description Sans-15px-black-70%'})
			resume_text = ''
			if resume_html:
				resume_text = resume_html.text.strip()
			resumes_pool.append(resume_text.replace('publication description\n', ''))
			#print 'Resume\n' + str(resume_text)
			# Get publication links
			#print 'Links:'
			#links_html = publis_block[n].findAll('a', href=True)
			links_html = item.findAll('a', href=True)
			publi_links = []
			if links_html:
				for m in range(0, len(links_html)):
					link_text = links_html[m]['href']
					if link_text not in publi_links:
						#print str(link_text.encode('utf-8'))
						publi_links.append(link_text)
			links_pool.append(publi_links)
		
	publications_data.append(titles_pool)
	publications_data.append(dates_pool)
	publications_data.append(journals_pool)
	publications_data.append(resumes_pool)
	publications_data.append(links_pool)
		
	return publications_data

def get_certifications_data(web_html):
	'''Recieves a LinkedIn profile html and returns a list with the certifications information.
	
	Parameters
	----------
	web_html
				Html code of a LinkedIn profile.
				
	Returns
	-------
	list
			[0] : Certification titles
			[1] : Dates of certification
			[2] : Issuing entities
	'''


	titles_pool         = []
	dates_pool          = []
	entities_pool       = []
	certifications_pool = []

	class_labels = ['pv-accomplishments-block__list ',
					'pv-accomplishments-block__list pv-accomplishments-block__list--has-more']
	
	certifications_section = web_html.find('section', attrs={'class':'accordion-panel pv-profile-section pv-accomplishments-block certifications pv-accomplishments-block--expanded ember-view'})
	for i in range(0, len(class_labels)):
		certifications_list    = certifications_section.find('ul', attrs={'class':class_labels[i]})
		if certifications_list:
			break

	if not certifications_list:
		print ('ERROR: certifications_list not found.')
		print ('Other uls found:')
		all_uls = certifications_section.find_all('ul')
		for i in range(0, len(all_uls)):
			try:
				print ('\t' + str(all_uls[i]['class']))
			except:
				pass
			
	for child in certifications_list.children:
		if len(child) > 1:
			item = BeautifulSoup(str(child), "html.parser")
			# Get title
			title_text = ''
			title_html = item.find('h4', attrs={'class':'pv-accomplishment-entity__title'})
			if title_html:
				title_text = title_html.text.strip()
			titles_pool.append(title_text.replace('Title', ''))
			# Get date
			date_text = ''
			date_html = item.find('p', attrs={'class':'pv-accomplishment-entity__subtitle'})
			if date_html:
				date_text = date_html.text.strip()
			dates_pool.append(date_text.replace('Certification Date' ,''))
			# Get certification entity
			entity_text = ''
			entity_html = item.find('a', attrs={'name':'certification_detail_company'})
			if entity_html:
				entity_text = entity_html.text.strip()
			entities_pool.append(entity_text)	
			
	certifications_pool.append(titles_pool)
	certifications_pool.append(dates_pool)
	certifications_pool.append(entities_pool)			

	return certifications_pool

def get_honors_data(web_html):
	'''Recieves a LinkedIn profile html and returns a list with the honors and awards information.
	
	Parameters
	----------
	web_html
				Html code of a LinkedIn profile.
				
	Returns
	-------
	list
			[0] : Awards titles
			[1] : Dates of awards
			[2] : Issuing entities
			[3] : Resumes of awards
	'''


	titles_pool   = []
	dates_pool    = []
	entities_pool = []
	resumes_pool  = []
	honors_pool   = []

	class_labels = ['pv-accomplishments-block__list ',
					'pv-accomplishments-block__list pv-accomplishments-block__list--has-more']

	
	honors_section = web_html.find('section', attrs={'class':'accordion-panel pv-profile-section pv-accomplishments-block honors pv-accomplishments-block--expanded ember-view'})
	for i in range(0, len(class_labels)):
		honors_list = honors_section.find('ul', attrs={'class':class_labels[i]})
		if honors_list:
			break
	
	if not honors_list:
		print ('ERROR: honors_list not found.')
		print ('Other uls found:')
		all_uls = honors_section.find_all('ul')
		for i in range(0, len(all_uls)):
			try:
				print ('\t' + str(all_uls[i]['class']))
			except:
				pass
	
	for child in honors_list.children:
		if len(child) > 1:
			item = BeautifulSoup(str(child), 'html.parser')
			
			# Get title
			title_text = ''
			title_html = item.find('h4', attrs={'class':'pv-accomplishment-entity__title'})
			if title_html:
				title_text = title_html.text.strip()
			titles_pool.append(title_text.replace('honor title', ''))
			# Get date
			date_text = ''
			date_html = item.find('span', attrs={'class':'pv-accomplishment-entity__date'})
			if date_html:
				date_text = date_html.text.strip()
			dates_pool.append(date_text.replace('honor date', ''))
			# Get entity
			entity_text = ''
			entity_html = item.find('span', attrs={'class':'pv-accomplishment-entity__issuer'})
			if entity_html:
				entity_text = entity_html.text.strip()
			entities_pool.append(entity_text.replace('honor issuer', ''))
			# Get resume
			resume_text = ''
			resume_html = item.find('p', attrs={'class':'pv-accomplishment-entity__description Sans-15px-black-70%'})
			if resume_html:
				resume_text = resume_html.text.strip()
			resumes_pool.append(resume_text.replace('honor description', ''))
	
	honors_pool.append(titles_pool)
	honors_pool.append(dates_pool)
	honors_pool.append(entities_pool)
	honors_pool.append(resumes_pool)
	return honors_pool
	
def get_languages_data(web_html):
	'''Recieves a LinkedIn profile html and returns a list with the languages information.
	
	Parameters
	----------
	web_html
				Html code of a LinkedIn profile.
				
	Returns
	-------
	list
			[0] : Languages
			[1] : Languages profiency
	'''


	languages_pool   = []
	proficiency_pool = []
	languages_data   = []

	class_labels = ['pv-accomplishments-block__list ',
					'pv-accomplishments-block__list pv-accomplishments-block__list--has-more']
	
	languages_section = web_html.find('section', attrs={'class':'accordion-panel pv-profile-section pv-accomplishments-block languages pv-accomplishments-block--expanded ember-view'})
	for i in range(0, len(class_labels)):
		languages_list = languages_section.find('ul', attrs={'class':class_labels[i]})
		if languages_list:
			break
	
	if not languages_list:
		print ('ERROR: languages_list not found.')
		print ('Other uls found:')
		all_uls = languages_section.find_all('ul')
		for i in range(0, len(all_uls)):
			try:
				print ('\t' + str(all_uls[i]['class']))
			except:
				pass
	
	for child in languages_list.children:
		if len(child) > 1:
			item = BeautifulSoup(str(child), 'html.parser')
			
			# Get language
			language_text = ''
			language_html = item.find('h4', attrs={'class':'pv-accomplishment-entity__title'})
			if language_html:
				language_text = language_html.text.strip()
			languages_pool.append(language_text.replace('Language name', ''))
			# Get proficiency
			proficiency_text = ''
			proficiency_html = item.find('p', attrs={'class':'pv-accomplishment-entity__proficiency pv-accomplishment-entity__subtitle'})
			if proficiency_html:
				proficiency_text = proficiency_html.text.strip()
			proficiency_pool.append(proficiency_text)
			
	languages_data.append(languages_pool)
	languages_data.append(proficiency_pool)
	
	return languages_data

def get_organizations_data(web_html):
	'''Recieves a LinkedIn profile html and returns a list with the organizations to which the candidate belongs to.
	
	Parameters
	----------
	web_html
				Html code of a LinkedIn profile.
				
	Returns
	-------
	list
			[0] : Organization names
			[1] : Dates at which the the candidate had belong to those organizations
			[2] : Positions inside the organizations
	'''


	names_pool         = []
	dates_pool         = []
	positions_pool     = []
	organizations_data = []

	class_labels = ['pv-accomplishments-block__list ',
					'pv-accomplishments-block__list pv-accomplishments-block__list--has-more']
	
	organization_section = web_html.find('section', attrs={'class':'accordion-panel pv-profile-section pv-accomplishments-block organizations pv-accomplishments-block--expanded ember-view'})
	for i in range(0, len(class_labels)):
		organization_list = organization_section.find('ul', attrs={'class':class_labels[i]})
		if organization_list:
			break
	
	if not organization_list:
		print ('ERROR: organization_list not found.')
		print ('Other uls found:')
		all_uls = organization_section.find_all('ul')
		for i in range(0, len(all_uls)):
			try:
				print ('\t' + str(all_uls[i]['class']))
			except:
				pass
	
	for child in organization_list.children:
		if len(child) > 1:
			# Create the html item
			item = BeautifulSoup(str(child), 'html.parser')
			# Get the name
			name_text = ''
			name_html = item.find('h4', attrs={'class':'pv-accomplishment-entity__title'})
			if name_html:
				name_text = name_html.text.strip()
			names_pool.append(name_text)
			# Get the dates
			date_text = ''
			date_html = item.find('span', attrs={'class':'pv-accomplishment-entity__subtitle'})
			if date_html:
				date_text = date_html.text.strip()
			dates_pool.append(date_text.replace('organization date', ''))
			# Get the position in the organization
			position_text = ''
			position_html = item.find('span', attrs={'class':'pv-accomplishment-entity__position'})
			if position_html:
				position_text = position_html.text.strip()
			positions_pool.append(position_text.replace('organization position', ''))

	organizations_data.append(names_pool)
	organizations_data.append(dates_pool)
	organizations_data.append(positions_pool)

	return organizations_data

def get_patents_data(web_html):
	'''Recieves a LinkedIn profile html and returns a list with the patents information.
	
	Parameters
	----------
	web_html
				Html code of a LinkedIn profile.
				
	Returns
	-------
	list
			[0] : Patent titles
			[1] : Dates of patents
			[2] : Patents references
			[3] : Resumes of patents
	'''


	titles_pool     = []
	dates_pool      = []
	references_pool = []
	resumes_pool    = []
	all_patents     = []

	class_labels = ['pv-accomplishments-block__list ',
					'pv-accomplishments-block__list pv-accomplishments-block__list--has-more']
	
	patents_section = web_html.find('section', attrs={'class':'accordion-panel pv-profile-section pv-accomplishments-block patents pv-accomplishments-block--expanded ember-view'})
	for i in range(0, len(class_labels)):
		patents_list = patents_section.find('ul', attrs={'class':class_labels[i]})
		if patents_list:
			break
	
	if not patents_list:
		print ('ERROR: patents_list not found.')
		print ('Other uls found:')
		all_uls = patents_section.find_all('ul')
		for i in range(0, len(all_uls)):
			try:
				print ('\t' + str(all_uls[i]['class']))
			except:
				pass
	
	
	for child in patents_list.children:
		if len(child) > 1:
			# Create html item
			item = BeautifulSoup(str(child), 'html.parser')
			# Get title
			title_text = ''
			title_html = item.find('h4', attrs={'class':'pv-accomplishment-entity__title'})
			if title_html:
				title_text = title_html.text.strip()
			titles_pool.append(title_text.replace('Patent title', ''))
			# Get the date
			date_text = ''
			date_html = item.find('span', attrs={'class':'pv-accomplishment-entity__date'})
			if date_html:
				date_text = date_html.text.strip()
			dates_pool.append(date_text.replace('Patent date', ''))
			# Get patent reference number
			reference_text = ''
			reference_html = item.find('span', attrs={'class':'pv-accomplishment-entity__issuer'})
			if reference_html:
				reference_text = reference_html.text.strip()
			references_pool.append(reference_text.replace('Patent issuer and number', ''))
			# Get the resume
			resume_text = ''
			resume_html = item.find('p', attrs={'class':'pv-accomplishment-entity__description Sans-15px-black-70%'})
			if resume_html:
				resume_text = resume_html.text.strip()
			resumes_pool.append(resume_text.replace('Patent description', ''))
	
	all_patents.append(titles_pool)
	all_patents.append(dates_pool)
	all_patents.append(references_pool)
	all_patents.append(resumes_pool)

	return all_patents
	

def get_projects_data(web_html):
	'''Recieves a LinkedIn profile html and returns a list with the projects information.
	
	Parameters
	----------
	web_html
				Html code of a LinkedIn profile.
				
	Returns
	-------
	list
			[0] : Projects titles
			[1] : Dates of projects
			[2] : Resumes of projects
			[3] : Links of projects
	'''


	titles_pool  = []
	dates_pool   = []
	resumes_pool = []
	links_pool   = []
	all_projects = []
	
	class_labels = ['pv-accomplishments-block__list ',
					'pv-accomplishments-block__list pv-accomplishments-block__list--has-more']
	
	projects_section = web_html.find('section', attrs={'class':'accordion-panel pv-profile-section pv-accomplishments-block projects pv-accomplishments-block--expanded ember-view'})
	#projects_list = projects_section.find('ul', attrs={'class':'pv-accomplishments-block__list '})
	
	for i in range(0, len(class_labels)):
		projects_list = projects_section.find('ul', attrs={'class':class_labels[i]})
		if projects_list:
			break
	
	if not projects_list:
		print ('ERROR: projects_list not found.')
		print ('Other uls found:')
		all_uls = projects_section.find_all('ul')
		for i in range(0, len(all_uls)):
			try:
				print ('\t' + str(all_uls[i]['class']))
			except:
				pass
	
	for child in projects_list.children:
		if len(child) > 1:
			# Create html item
			item = BeautifulSoup(str(child), 'html.parser')
			# Get title
			title_text = ''
			title_html = item.find('h4', attrs={'class':'pv-accomplishment-entity__title'})
			if title_html:
				title_text = title_html.text.strip()
			titles_pool.append(title_text.replace('Project name', ''))
			# Get date
			date_text = ''
			date_html = item.find('p', attrs={'class':'pv-accomplishment-entity__date pv-accomplishment-entity__subtitle'})
			if date_html:
				date_text = date_html.text.strip()
			dates_pool.append(date_text)
			# Get resume
			resume_text = ''
			resume_html = item.find('p', attrs={'class':'pv-accomplishment-entity__description Sans-15px-black-70%'})
			if resume_html:
				resume_text = resume_html.text.strip()
				if resume_text == '':
					resume_text = item.text.strip()
			resumes_pool.append(resume_text)
			# Get links
			project_links = []
			link_text = ''
			links_html = item.findAll('a', href=True)
			if links_html:
				for link in links_html:
					link_text = link['href']
					if link_text not in project_links:
						project_links.append(link_text)
			links_pool.append(project_links)
			
	all_projects.append(titles_pool)
	all_projects.append(dates_pool)
	all_projects.append(resumes_pool)
	all_projects.append(links_pool)
	
	return all_projects

def get_course_data(web_html):
	'''Recieves a LinkedIn profile html and returns a list with the courses information.
	
	Parameters
	----------
	web_html
				Html code of a LinkedIn profile.
				
	Returns
	-------
	list
			[0] : Courses titles
			[1] : Other information about the courses
	'''


	titles_pool = []
	extras_pool = []
	all_courses = []

	class_labels = ['pv-accomplishments-block__list ',
					'pv-accomplishments-block__list pv-accomplishments-block__list--has-more']
	
	course_section = web_html.find('section', attrs={'class':'accordion-panel pv-profile-section pv-accomplishments-block courses pv-accomplishments-block--expanded ember-view'})
	for i in range(0, len(class_labels)):
		projects_list = course_section.find('ul', attrs={'class':class_labels[i]})
		if course_list:
			break
	
	if not course_list:
		print ('ERROR: course_list not found.')
		print ('Other uls found:')
		all_uls = course_section.find_all('ul')
		for i in range(0, len(all_uls)):
			try:
				print ('\t' + str(all_uls[i]['class']))
			except:
				pass
	
	for child in course_list.children:
		if len(child) > 1:
			# Create html item
			item = BeautifulSoup(str(child), 'html.parser')
			# Get title
			title_text = ''
			title_html = item.find('h4', attrs={'class':'pv-accomplishment-entity__title'})
			if title_html:
				title_text = title_html.text.strip()
			titles_pool.append(title_text.replace('Course name', ''))
			# Get extra info
			extra_text = ''
			extra_html = item.find('p', attrs={'class':'pv-accomplishment-entity__course-number pv-accomplishment-entity__subtitle'})
			if extra_html:
				extra_text = extra_html.text.strip()
			extras_pool.append(extra_text.replace('Course number', ''))
	
	all_courses.append(titles_pool)
	all_courses.append(extras_pool)
			
	return all_courses
	
def get_test_scores_data(web_html):
	'''Recieves a LinkedIn profile html and returns a list with the scorers information.
	
	Parameters
	----------
	web_html
				Html code of a LinkedIn profile.
				
	Returns
	-------
	list
			[0] : Titles
			[1] : Dates
			[2] : Scorers
			[3] : Resumes of scorers
	'''


	titles_pool  = []
	dates_pool   = []
	scorers_pool = []
	resumes_pool = []
	all_scorers  = []

	class_labels = ['pv-accomplishments-block__list ',
					'pv-accomplishments-block__list pv-accomplishments-block__list--has-more']
	
	scorers_section = web_html.find('section', attrs={'class':'accordion-panel pv-profile-section pv-accomplishments-block test-scores pv-accomplishments-block--expanded ember-view'})
	for i in range(0, len(class_labels)):
		scorers_list = scorers_section.find('ul', attrs={'class':class_labels[i]})
		if scorers_list:
			break
	
	if not scorers_list:
		print ('ERROR: scorers_list not found.')
		print ('Other uls found:')
		all_uls = scorers_section.find_all('ul')
		for i in range(0, len(all_uls)):
			try:
				print ('\t' + str(all_uls[i]['class']))
			except:
				pass
	
	for child in scorers_list.children:
		if len(child) > 1:
			# Create html item
			item = BeautifulSoup(str(child), 'html.parser')
			# Get title
			title_text = ''
			title_html = item.find('h4', attrs={'class':'pv-accomplishment-entity__title'})
			if title_html:
				title_text = title_html.text.strip()
			titles_pool.append(title_text.replace('Test name', ''))
			# Get date
			date_text = ''
			date_html = item.find('span', attrs={'class':'pv-accomplishment-entity__date'})
			if date_html:
				date_text = date_html.text.strip()
				date_broken = date_text.split('\n')
				date_text = date_broken[1]
			dates_pool.append(date_text)
			# Get scorers
			scorer_text = ''
			scorer_html = item.find('span', attrs={'class':'pv-accomplishment-entity__score'})
			if scorer_html:
				scorer_text = scorer_html.text.strip()
			scorers_pool.append(scorer_text)
			# Get resume
			resume_text = ''
			resume_html = item.find('p', attrs={'class':'pv-accomplishment-entity__description Sans-15px-black-70%'})
			if resume_html:
				resume_text = resume_html.text.strip()
			resumes_pool.append(resume_text)
	
	all_scorers.append(titles_pool)
	all_scorers.append(dates_pool)
	all_scorers.append(scorers_pool)
	all_scorers.append(resumes_pool)

	return all_scorers
	
def get_interests_from_profile(web_html):
	'''Recieves a LinkedIn profile html and returns a list with the interests.
	
	Parameters
	----------
	web_html
				Html code of a LinkedIn profile.
				
	Returns
	-------
	list
			[0] : Interests titles
			[1] : Interests number of followers
	'''


	interest_followers = []
	interests = []
	followers = []

	interests_block_html = web_html.find('section', attrs={'class':'pv-profile-section pv-interests-section artdeco-container-card ember-view'})
	interests_html = interests_block_html.findAll('li', attrs={'class':'pv-interest-entity pv-profile-section__card-item ember-view'})
	for i in range(0, len(interests_html)):
		interest_name_html = interests_html[i].find('h3', attrs={'class':'pv-entity__summary-title Sans-17px-black-85%-semibold'})
		interest_name_text = interest_name_html.text.strip()
		interests.append(interest_name_text)
		#print interest_name_text
		followers_html = interests_html[i].find('p', attrs={'class':'pv-entity__follower-count Sans-15px-black-55%'})
		followers_text = followers_html.text.strip()
		no_followers = followers_text.replace('followers', '')
		no_follower  =   no_followers.replace('follower', '')
		no_members   =    no_follower.replace('members', '')
		no_member    =     no_members.replace('member', '')
		no_space     =      no_member.replace(' ', '')
		no_coma      =       no_space.replace(',', '')
		#print no_coma
		followers.append(no_coma)
		#print ''
	interest_followers.append(interests)
	interest_followers.append(followers)
	return interest_followers
	
def interest_pages(web_html):

	## Check the docs

	'''Checks if there are more interests'''
	extra_interests = False
	match = re.search(r'/detail/interests/' , str(web_html))
	if match:
		extra_interests = True
	return extra_interests
	
def get_extra_interests(web_html):
	'''Recieves the html of the expanded see all interests and returns a list with the interests and the number of followers.
	
	Parameters
	----------
	web_html
				Html code of a LinkedIn profile.
				
	Returns
	-------
	list
			[0] : Interests titles
			[1] : Interests number of followers
	'''


	interest_followers = []
	interests = []
	followers = []

	interests_block_html = web_html.findAll('li', attrs={'class':' entity-list-item'})
	if interests_block_html:
		for i in range(0, len(interests_block_html)):
			interest_name_html = interests_block_html[i].find('span', attrs={'class':'pv-entity__summary-title-text'})
			interest_name_text = interest_name_html.text.strip()
			#print interest_name_text.encode('utf-8')
			interests.append(interest_name_text)
			followers_html = interests_block_html[i].find('p', attrs={'class':'pv-entity__follower-count Sans-15px-black-55%'})
			followers_text = followers_html.text.strip()
			no_followers = followers_text.replace('followers', '')
			no_follower  =   no_followers.replace('follower', '')
			no_members   =    no_follower.replace('members', '')
			no_member    =     no_members.replace('member', '')
			no_space     =      no_member.replace(' ', '')
			no_coma      =       no_space.replace(',', '')
			followers.append(no_coma)
			#print no_coma.encode('utf-8')
	interest_followers.append(interests)
	interest_followers.append(followers)

	return interest_followers

def get_posts(web_html):
	'''Recieves a LinkedIn profile activity information, returns a list of the articles, posts and liked posts shown.
	The function identifies the posts and sends the posts html to the function analyse_post.
	The three lists return content the information extracted by analyse_post.
	
	Parameters
	----------
	web_html
				Html code of a LinkedIn profile.
				
	Returns
	-------
	list
			[0] : Articles written
					[0] : Post text
					[1] : Post titles
					[2] : Shared link
					[3] : Number of likes
					[4] : Number of comments
			[1] : Posts written
					[0] : Post text
					[1] : Post titles
					[2] : Shared link
					[3] : Number of likes
					[4] : Number of comments
			[2] : Liked posts
					[0] : Post text
					[1] : Post titles
					[2] : Shared link
					[3] : Number of likes
					[4] : Number of comments
	'''

	articles_labels = [ 'feed-base-update mh0 Elevation-2dp relative feed-base-update--reshare reshare-update ember-view',
						'feed-base-update mh0 Elevation-2dp relative feed-base-update--channel channel-update article ember-view',
						'feed-base-update mh0 Elevation-2dp relative feed-base-update--viral viral-update article ember-view']
	
	
	articles_pool = []
	posts_pool    = []
	liked_pool    = []
	all_activity  = []

	articles_flag    = False
	posts_flag       = False
	liked_posts_flag = False
	
	name_html = web_html.find('span', attrs={'class':'hoverable-link-text'})
	if name_html:
		name_text = name_html.text.strip()
	
	voyager_feed = web_html.find('div', attrs={'class':'pv-recent-activity-detail__feed-container feed-container-theme ember-view'})
		
	if voyager_feed:
		articles_stack = voyager_feed.find_all('article')
		print ('Number of activity posts: ' + str(len(articles_stack)))
		for i in range(0, len(articles_stack)):
			if 'mh0' in articles_stack[i]['class']:
				bar_html = articles_stack[i].find('div', attrs={'class':'feed-base-top-bar Sans-13px-black-70% ember-view'})
				if bar_html:
					breaken_bar = bar_html.text.strip().split(' ')
					if ('likes' in breaken_bar) or ('liked' in breaken_bar):
						# This are liked posts
						liked_posts_flag = True
						liked_post = analyse_post(articles_stack[i])
						liked_pool.append(liked_post)
					if 'commented' in breaken_bar:
						# This is a commented post (not been retrieved at the moment)
						pass
					if 'replied' in breaken_bar:
						# This is a replied to a comment (not been retrieved at the moment)
						pass
				if not bar_html:
					# Get source
					source_text = ''
					#source_html = articles_stack[i].find('h3', attrs={'class':'feed-s-image-description__byline Sans-13px-black-55%'})
					source_html = articles_stack[i].find('h3', attrs={'class':'feed-base-image-description__byline Sans-13px-black-55%'})
					if source_html:
						source_text = source_html.text.strip()
					if source_text:
						source_no_linkedin = source_text.replace(' on LinkedIn', '')
						if source_no_linkedin == name_text:
							# This are articles written by the candidate
							articles_flag = True
							article = analyse_post(articles_stack[i])
							articles_stack.append(article)
						if source_no_linkedin != name_text:
							# This is a post
							posts_flag = True
							post = analyse_post(articles_stack[i])
							posts_pool.append(post)
					if source_text == '':
						# This are also posts
						post = analyse_post(articles_stack[i])
						posts_pool.append(post)	
	
	if articles_flag == False:
		empty_article = ['NULL', 'NULL', 'NULL', 'NULL', 'NULL']
		articles_pool.append(empty_article)
	if posts_flag == False:
		empty_post = ['NULL', 'NULL', 'NULL', 'NULL', 'NULL']
		posts_pool.append(empty_post)
	if liked_posts_flag == False:
		empty_like = ['NULL', 'NULL', 'NULL', 'NULL', 'NULL']
		liked_pool.append(empty_like)	
	
	all_activity.append(articles_pool)
	all_activity.append(posts_pool)
	all_activity.append(liked_pool)
	
	return all_activity

	
	
	
def analyse_post(post_html):
	'''Recieves the html of a post, returns information about that post.
	
	Parameters
	----------
	web_html
				Html code of a LinkedIn profile.
				
	Returns
	-------
	list
			[0] : Post text
			[1] : Post titles
			[2] : Shared link
			[3] : Number of likes
			[4] : Number of comments
	'''

	texts_pool    = []
	titles_pool   = []
	sources_pool  = []
	likes_pool    = []
	comments_pool = []
	post_data     = []
	
	#all_divis = post_html.find_all('div')
	#for i in range(0, len(all_divis)):
	#	try:
	#		print (all_divis[i]['class'])
	#	except:
	#		pass
	
	
	labels_pool = [ 'feed-s-update__description feed-s-inline-show-more-text ember-view',
					'feed-base-update__description feed-base-inline-show-more-text ember-view',
					'feed-base-update__description feed-base-inline-show-more-text is-empty ember-view',
					'feed-base-inline-show-more-text is-empty ember-view',
					'feed-base-inline-show-more-text ember-view']
	
	# Get text
	text = 'NULL'	
	for i in range(0, len(labels_pool)):
		text_html = post_html.find('div', attrs={'class':labels_pool[i]})
		if text_html:
			item_text = text_html.text.strip()
			if item_text:
				text = unicodetoascii(item_text)
			break
	
	if text == 'NULL':		
		text_html = post_html.find('p', attrs={'class':'feed-base-main-content--mini-update Sans-15px-black-70% feed-base-main-content ember-view'})
		if text_html:
			item_text = text_html.text.strip()
			if item_text:
				text = unicodetoascii(item_text)

	original_html = post_html.find('span', attrs={'data-control-name':'original_share'})
	if original_html:
		original_text = original_html.text.strip()
		if item_text:
			text = unicodetoascii(original_text)
			
	texts_pool.append(text)
	# Title shared
	title_text = 'NULL'
	title_html = post_html.find('h2', attrs={'class':'feed-base-image-description__headline Sans-15px-black-85%-semibold'})
	if title_html:
		title_text = title_html.text.strip()
	
	title_text = unicodetoascii(title_text)
	titles_pool.append(title_text)
	# Get source
	source_text = 'NULL'
	source_html = post_html.find('h3', attrs={'class':'feed-base-image-description__byline Sans-13px-black-55%'})
	if source_html:
		source_text = source_html.text.strip()
	source_text = unicodetoascii(source_text)
	sources_pool.append(source_text)
	# Get number of likes and number of comments
	likes_number = '0'
	likes_html = post_html.find('button', attrs={'class':'feed-base-social-counts__num-likes feed-base-social-counts__count-value Sans-13px-black-55% hoverable-link-text'})
	if likes_html:
		like_spans = likes_html.find_all('span')
		likes_text = like_spans[0].text.strip()
		likes_number = re.findall('\d+', str(likes_text))[0]
	
	comments_number = '0'
	comments_html = post_html.find('button', attrs={'class':'feed-base-social-counts__num-comments feed-base-social-counts__count-value Sans-13px-black-55% hoverable-link-text'})
	if comments_html:
		comment_spans = comments_html.find_all('span')
		comment_text = comment_spans[0].text.strip()
		comments_number = re.findall('\d+', str(comment_text))[0]
	
	
	numbers_block = post_html.find('ul', attrs={'class':'feed-s-social-counts ember-view'})
	if numbers_block:
		for item in numbers_block.children:
			if len(item) > 1:
				cosa = BeautifulSoup(str(item), 'html.parser')
				button_html = cosa.find('button')
				span_one = button_html.find('span')
				span_text = span_one.text.strip()
				span_broken = span_text.split(' ')
				span_number = span_broken[0].replace(',', '')
				if button_html['data-control-name'] == 'likes_count':
					likes_number = span_number
				if button_html['data-control-name'] == 'comments_count':
					comments_number = span_number
	likes_pool.append(likes_number)
	comments_pool.append(comments_number)
	
	post_data.append(text)
	post_data.append(title_text)
	post_data.append(source_text)
	post_data.append(likes_number)
	post_data.append(comments_number)
	
	return post_data

def get_followers_number(web_html):
	'''Recieves a LinkedIn profile activity html returns the number of followers.
	
	Parameters
	----------
	web_html
				Html code of a LinkedIn profile.
				
	Returns
	-------
	str
				Number of followers, NULL if none.
	'''

	followers_number = '0'
	side_box = web_html.find('aside', attrs={'class':'pv-recent-activity-detail__left-rail left-rail'})
	if side_box:
		followers_html = side_box.find('p', attrs={'class':'pv-recent-activity-top-card__follower-count Sans-15px-black-70%'})
		if followers_html:
			followers_text = followers_html.text.strip()
			no_followers = followers_text.replace('Followers', '')
			no_follower  =   no_followers.replace('Follower', '')
			followers_number = str(no_follower)
	
	return followers_number

def unicodetoascii(text):
# http://www.utf8-chartable.de/unicode-utf8-table.pl?start=8192&number=128&utf8=string-literal

    TEXT = (text.
			replace('\\n', ' ').
    		replace('\\xe2\\x80\\x99', "'").
    		replace('\xe2\x80\x99',    "'").
            replace('\\xc3\\xa9',      'e').
            replace('\xc3\xa9',        'e').
            replace('\\xe2\\x80\\x90', '-').
            replace('\xe2\x80\x90',    '-').
            replace('\\xe2\\x80\\x91', '-').
            replace('\xe2\x80\x91',    '-').
            replace('\\xe2\\x80\\x92', '-').
            replace('\xe2\x80\x92',    '-').
            replace('\\xe2\\x80\\x93', '-').
            replace('\xe2\x80\x93',    '-').
            replace('\\xe2\\x80\\x94', '-').
            replace('\xe2\\x80\x94',   '-').
            replace('\\xe2\\x80\\x98', "'").
            replace('\xe2\x80\x98',    "'").
            replace('\\xe2\\x80\\x99', "'").
            replace('\xe2\x80\x99',    "'").
            replace('\\xe2\\x80\\x9b', "'").
            replace('\xe2\x80\x9b',    "'").
            replace('\\xe2\\x80\\x9c', '"').
            replace('\xe2\x80\x9c',    '"').
            replace('\\xe2\\x80\\x9d', '"').
            replace('\xe2\x80\x9d',    '"').
            replace('\\xe2\\x80\\x9e', '"').
            replace('\xe2\x80\x9e',    '"').
            replace('\\xe2\\x80\\x9f', '"').
            replace('\xe2\x80\x9f',    '"').
            replace('\\xe2\\x80\\xa6', '...').
            replace('\xe2\x80\xa6',    '...').
            replace('\\xe2\\x80\\xb2', "'").
            replace('\xe2\x80\xb2',    "'").
            replace('\\xe2\\x80\\xb3', "'").
            replace('\xe2\x80\xb3',    "'").
            replace('\\xe2\\x80\\xb4', "'").
            replace('\xe2\x80\xb4',    "'").
            replace('\\xe2\\x80\\xb5', "'").
            replace('\xe2\x80\xb5',    "'").
            replace('\\xe2\\x80\\xb6', "'").
            replace('\xe2\x80\xb6',    "'").
            replace('\\xe2\\x80\\xb7', "'").
            replace('\xe2\x80\xb7',    "'").
            replace('\\xe2\\x81\\xba', "+").
            replace('\xe2\x81\xba',    "+").
            replace('\\xe2\\x81\\xbb', "-").
            replace('\xe2\x81\xbb',    "-").
            replace('\\xe2\\x81\\xbc', "=").
            replace('\xe2\x81\xbc',    "=").
            replace('\\xe2\\x81\\xbd', "(").
            replace('\xe2\x81\xbd',    "(").
            replace('\\xe2\\x81\\xbe', ")").
            replace('\xe2\x81\xbe',    ")").
            replace('\\xc2\\xa0',       "").
            replace('\xc2\xa0',         "").
			replace('\n', ' ').
			replace('\\', '')
                 )
	
    while '  ' in TEXT:
        TEXT = TEXT.replace('  ', ' ')

    if TEXT[0] == ' ':
        TEXT = TEXT[1:]
    try:
        if TEXT[-1] == ' ':
            TEXT = TEXT[:-1]
    except:
        pass
		
		
    return TEXT
	
if __name__=="__main__":
	print ('Hi')