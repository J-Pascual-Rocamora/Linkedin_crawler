# Soup Handler
import os
import re
import urlparse
from bs4 import BeautifulSoup


def get_profiles(web_html):
	'''Retrieves linkedin profile links from a web.
	
	Parameters
	----------
	web_html
				Html of a Linkedin seaerch page web page.
		
	Returns
	--------
	list 
			Profile links.

	'''
			
	# Recieves web_html and returns the profile links on it
	profiles = []
	url_head = 'https://www.linkedin.com'
	# Get all links on the webpage
	for link in web_html.find_all('a', href=True):
		# Filter links
		if re.findall('/in/', str(link)):
			# Create full link and add to the list
			url = url_head + str(link['href'])
			profiles.append(url)
	return profiles
	
def match_date(web_html, year):
	'''Checks if the year requirement is meet. 
	Gets the year at which the candidate started his current job. 
	Compares this to the requirement and returns true or false.
	Currently not in use.
	
	Parameters
	----------
	web_html
				Linkedin profile html code
	year
				Requiremed year of current job beginning.
		
	Returns
	-------
	bool. 
				True if the requierement is met. False otherwise.
	
    '''
	
	# Check the date at which the current job was started
	match = False
	bkg = web_html.find('span', attrs={'class':'background-details'})
	fecha = re.findall('(?<=<span>).+(?=Present)', str(bkg))
	date = re.findall(str(year), str(fecha))
	if date:
		match = True
	return match

def get_info(soup):
	'''Extracts profile information.
	This is an old method and its not used currently.
		
	Parameters
	----------
	soup
			Html of a Linkedin profile webpage.
	
	Returns
	-------
	list
			[0] Name
			[1] Current position
			[2] Current company
			[3] Date of current job beginning
			[4] Current location

    '''
	
	# Get the info from the header text
	fecha = []
	info = []
	resume = soup.find('div', attrs={'class':'pv-top-card-section__information mt3'})
	try:
		name = soup.find('h1')
		nombre =  re.findall('(?<=>).+(?=<\/h1>)', str(name))
		info.append(nombre[0])
	except:
		try:
			info.append(nombre)
		except:
			info.append('-')
	
	try:
		position = soup.find('h2')
		pos =  re.findall('(?<=>).+(?=<\/h2>)', str(position))
		info.append(pos[0])
	except:
		try:
			info.append(pos)
		except:
			info.append('-')
			
	try:
		others = soup.findAll('h3')
		company = str(others[0])
		info.append(company[89:-14])
	except:
		info.append('-')
	
	try:	
		bkg = soup.find('span', attrs={'class':'background-details'})
		date = re.findall('(?<=<span>).+(?=Present)', str(bkg))
		date = str(date)
		fecha = date[2:10]
		if re.findall('xe', str(fecha)):
			date_short = fecha[:4]
			fecha = date_short
		info.append(fecha)
	except:
		info.append('-')
	
	try:
		lugar   = re.findall('(?<=>).+(?=<\/h3>)', str(others[2]))
		info.append(lugar[0])
	except:
		try:
			info.append(lugar)
		except:
			info.append('-')
	
	return info

def get_experience(soup):
	'''Gets the employment information.
	This is an old function. Not in use currently
	
	Parameters
	----------
	soup
			Html of a Linkedin profile.
		
	Returns
	-------
	list
			Information about all posisions
			[0] Position
			[1] Company
			[2] Date
			[3] Location

    '''
	
	# Get the experience information from the html
	jobs = []
	experience = soup.find('section', attrs={'class':'pv-profile-section experience-section ember-view'})
	text = experience.findAll('li')
	n = 0
	for item in text:
		new = []
		jobs.append(new)
		position = item.find('h3')
		pos  =  re.findall('(?<=>).+(?=<\/h3>)', str(position))
		comp = item.find('span', attrs={'class':'pv-entity__secondary-title'})
		company = re.findall('(?<=>).+(?=<\/span>)', str(comp))
		dates = item.find('h4', attrs={'class':'pv-entity__date-range inline-block Sans-15px-black-70%'})
		date = re.findall('(?<=<span>).+(?=<\/span>)', str(dates))
		place = item.find('h4', attrs={'class':'pv-entity__location Sans-15px-black-70% block'})
		location = re.findall('(?<=<span>).+(?=<\/span>)', str(place))
		resume = item.find('p', attrs={'class':'pv-entity__description Sans-15px-black-70% mt4'})
		resume = str(resume)
		text = resume[65:-9]
		final = text.replace('<br/>','\n')
		jobs[n].append(str(pos[0]))
		jobs[n].append(str(company[0]))
		jobs[n].append(str(date[0]))
		try:
			jobs[n].append(str(location[0]))
		except:
			jobs[n].append('-')
		jobs[n].append(str(final))
		n = n + 1
	
	return jobs
	
if __name__=="__main__":

	print 'Hey this is been run'