import os, time, random, sys
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException

from . import data
from . import profile_html_handler



def open_browser():
	'''Opens Firefox (might want to improve the headers)'''
	#Start browser
	browser = webdriver.Firefox()
	time.sleep(random.uniform(3.5, 6.9))

	return browser

def open_headless():

	# Two below are needed for headless firefox
	from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
	os.environ['MOZ_HEADLESS'] = '1'

	# Select your Firefox binary.
	binary = FirefoxBinary('C:\\Program Files\\Mozilla Firefox\\firefox.exe', log_file=sys.stdout)

	# Start selenium with the configured binary.
	browser = webdriver.Firefox(firefox_binary=binary)

	return browser

def open_chrome():

	from seleniumrequests import Chrome
	#from pyvirtualdisplay import Display

	#display = Display(visible=0, size=(1440, 900))
	#display.start()
	browser = Chrome()

	print('Chrome browser opened succesfully')

	return browser

def open_phantom():
	'''Opens phantom browser'''
	# https://stackoverflow.com/questions/35666067/selenium-phantomjs-custom-headers-in-python

	phantomjs_path = r"C:\Program Files\phantomjs-2.1.1\bin\bin\phantomjs.exe"

	headers = { 'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Encoding':'gzip, deflate',
    'Accept-Language':'en-US,en;q=0.5',
    'Cache-Control':'max-age=0',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:54.0) Gecko/20100101 Firefox/54.0.1'
	}

	for key, value in enumerate(headers):
		capability_key = 'phantomjs.page.customHeaders.{}'.format(key)
		webdriver.DesiredCapabilities.PHANTOMJS[capability_key] = value

	browser = webdriver.PhantomJS(executable_path=phantomjs_path,service_args=['--ignore-ssl-errors=true'])
	browser.set_window_size(1124, 850)
		
	return browser
	
def logeate(browser):
	'''Opens LinkedIn and logs into the account.
	
	Parameters
	----------
	browser
				Driver element
	'''

	try:
		# Open linkedin
		#browser.get('https://www.linkedin.com/uas/login')
		browser.get('https://www.linkedin.com')
		time.sleep(random.uniform(1.5, 3.9))
		# Login
		#emailElement = browser.find_element_by_id('session_key-login')
		emailElement = browser.find_element_by_id('login-email')
		emailElement.send_keys(data.lnkd_dat[0])
		time.sleep(random.uniform(3.5, 6.9))
		#passElement = browser.find_element_by_id('session_password-login')
		passElement = browser.find_element_by_id('login-password')
		passElement.send_keys(data.lnkd_dat[1])
		passElement.submit()
		print('1st logging attempt was succesfull')
		time.sleep(random.uniform(0.7, 1.3))

	except Exception as e:
		print('ERROR: First logging method failed')
		print(e)
		web_html = get_the_soup(browser)
		save_the_soup(web_html, 'failed_logging_attempt')
		# Try to login on a different url
		browser.get('https://www.linkedin.com/home')
		time.sleep(random.uniform(1.5, 3.9))
		#Login
		emailElement = browser.find_element_by_id('login-email')
		emailElement.send_keys(data.lnkd_dat[0])
		time.sleep(random.uniform(3.5, 6.9))
		passElement = browser.find_element_by_id('login-password')
		passElement.send_keys(data.lnkd_dat[1])
		passElement.submit()
	time.sleep(random.uniform(3.5, 6.9))

	return 

def scroll_to_bottom(browser):
	'''Scrolls to the bottom of the current page.
	
	Parameters
	----------
	browser
				Driver element.
	
	'''
	
	SCROLL_PAUSE_TIME = 1.5
	# Get scroll height
	last_height = browser.execute_script("return document.body.scrollHeight")
	print ('Scrolling to bottom')
	while True:
		# Scroll down to bottom
		for i in range(0, 10):
			browser.execute_script("window.scrollBy(0, 300);")
			time.sleep(random.uniform(0.3, 0.7))
		# Wait to load page
		time.sleep(SCROLL_PAUSE_TIME)
		# Calculate new scroll height and compare with last scroll height
		new_height = browser.execute_script("return document.body.scrollHeight")
		if new_height == last_height:
			break
		last_height = new_height
	return

def scroll_to_experience(browser):
	'''Scroll to the beginning of the experience section (currently not in use)'''
	time.sleep(random.uniform(0.5, 1.1))
	# Get the position of the experience element
	experience_element = browser.find_element_by_xpath("//header[@class='pv-profile-section__card-header']")
	experience_position = experience_element.location
	command = 'window.scrollTo('+ str(experience_position) + ', document.body.scrollHeight);'
	browser.execute_script(command)
	return

def scroll_to_education(browser):
	'''Scroll to the beginning of the education section (currently not in use)'''
	time.sleep(random.uniform(0.5, 1.1))
	# Get the position of the experience element
	experience_element = browser.find_element_by_xpath("/html/body/div[5]/div[4]/div[2]/div/div/div/div[2]/div[1]/div[2]/div[4]/span/section/section[2]/header[@class='pv-profile-section__card-header']")
	experience_position = experience_element.location
	command = 'window.scrollTo('+ str(experience_position) + ', document.body.scrollHeight);'
	browser.execute_script(command)
	return

def scroll_to_item(browser, xpath):
	'''Scroll to the item given by the xpath provided.

	Parameters
	----------
	browser
				Driver element.

	xpath
				String with the desired element xpath.

	'''


	time.sleep(random.uniform(0.5, 1.1))
	# Get the position of the experience element
	experience_element = browser.find_element_by_xpath(xpath)
	experience_position = experience_element.location
	command = 'window.scrollTo('+ str(experience_position) + ', document.body.scrollHeight);'
	browser.execute_script(command)
	return
	
def expand_other_links(browser):
	'''Expands the menu where other links are displayed.

	Parameters
	----------
	browser
				Driver element.

	'''


	print ('Expanding other links section')
	try:
		element = browser.find_element_by_xpath("//button[@class='contact-see-more-less link-without-visited-state']")
		if element:
			#element.click()
			browser.execute_script("arguments[0].click();", element)
			print ('Other links section expanded')
	except:
		print ('Other links button not found')
		pass

	return	

def expand_all(browser):
	'''Expand experience and education sections.
	
	Parameters
	----------
	browser
				Driver element.
	
	'''
	
	
	try:
		while browser.find_element_by_xpath("//button[@class='pv-profile-section__see-more-inline link']"):
			#browser.find_element_by_xpath("//button[@class='pv-profile-section__see-more-inline link']").click()
			button_element = browser.find_element_by_xpath("//button[@class='pv-profile-section__see-more-inline link']")
			browser.execute_script("arguments[0].click();", button_element)
			time.sleep(random.uniform(0.5, 0.9))
	except NoSuchElementException:
		print ('No more expadable buttons')
		pass
	except ElementNotInteractableException:
		print ('Element no interactable')
		pass
	return

def expand_summary(browser):
	'''Expands the summary on top of the profile.
	
	Parameters
	----------
	browser
				Driver element.
	
	'''
	
	
	buttons = browser.find_elements_by_xpath("//button[@class='pv-top-card-section__summary-toggle-button button-tertiary-small mt4']")
	if buttons:
		#buttons[0].click()
		button_element = buttons[0]
		browser.execute_script("arguments[0].click();", button_element)
	return

def expand_skills(browser):
	'''Expand the skills section.
	
	Parameters
	----------
	browser
				Driver element.
	
	'''
	

	all_classes = ['pv-profile-section__card-action-bar artdeco-container-card-action-bar pv-skills-section__additional-skills',
					'pv-profile-section__card-action-bar pv-skills-section__additional-skills artdeco-container-card-action-bar',
					'artdeco-container-card-action-bar pv-profile-section__card-action-bar pv-skills-section__additional-skills',
					'artdeco-container-card-action-bar pv-skills-section__additional-skills pv-profile-section__card-action-bar',
					'pv-skills-section__additional-skills pv-profile-section__card-action-bar artdeco-container-card-action-bar',
					'pv-skills-section__additional-skills artdeco-container-card-action-bar pv-profile-section__card-action-bar']
	
	for i in range(0, len(all_classes)):
		button_xpath = '//button[@class=\'' + str(all_classes[i]) + '\']'
		print (button_xpath)
		buttons = browser.find_elements_by_xpath(button_xpath)
		if buttons:
			#buttons[0].click()
			button_element = buttons[0]
			browser.execute_script("arguments[0].click();", button_element)
			time.sleep(random.uniform(0.5, 0.9))
			print ('Skills expanded')
			break
			
	return

def expand_header(browser):
	'''Expand the resume section in the header.
	
	Parameters
	----------
	browser
				Driver element.
	
	'''


	try:
		#browser.find_element_by_xpath("//button[@class='pv-top-card-section__summary-toggle-button button-tertiary-small mt4']").click()
		button_element = browser.find_element_by_xpath("//button[@class='pv-top-card-section__summary-toggle-button button-tertiary-small mt4']")
		browser.execute_script("arguments[0].click()", button_element)
	except NoSuchElementException:
		print ('No resume to be expanded')
		pass
	return

def expand_all_activity(browser):
	'''Expands all activity.
	
	Parameters
	----------
	browser
				Driver element.
	
	'''


	try:
		expandable_buttons = browser.find_elements_by_xpath("//button[@class='see-more Sans-15px-black-55% hoverable-link-text']")
		for button in expandable_buttons:
			#button.click()
			browser.execute_script("arguments[0].click();", button)
	except:
		print ('No more expandable buttons')
	
	return
	
#def expand_all_accomplishments(browser):
#	'''Not in use'''
#	buttons = browser.find_elements_by_xpath("//button[@class='pv-accomplishments-block__expand']")
#	for i in range(0, len(buttons)):
#	#	element_start = "/html/body/div[5]/div[3]/div[2]/div/div/div/div[2]/div[1]/div[2]/div[7]/section/section["
#	#	element_end   = "]/div[@class='pv-accomplishments-block__expand']"
#	#	element       = element_start + str(i+1) + element_end
#	#	print element
#	#	button = browser.find_element_by_xpath(element)
#	#	button.click()
#		#flechitas = browser.find_elements_by_xpath(element)
#		#button_position = button.location
#		#command = 'window.scrollTo('+ str(button_position) + ', document.body.scrollHeight);'
#		#browser.execute_script(command)
#		#if flechitas:
#		#	flechitas[0].click()
#		attribute_name = buttons[i].get_attribute("data-control-name")
#		print ('data-control-name: ' + str(attribute_name))
#		broken_attribute = str(attribute_name.split('_'))
#		if 'expand' in broken_attribute:
#			print ('Clicking')
#			#buttons[i].click()
#			button_element = buttons[i]
#			browser.execute_script("arguments[0].click();", button_element)
#			time.sleep(random.uniform(2.5, 3.1))
#	print ('Total chevrons found: ' + str(len(buttons)))
#
#	return

def click_that_accomplishment_button(browser, button_label):
	'''Clicks the accomplishment button which data-control-name label is equal to the variable button_label.
	
	Parameters
	----------
	browser
				Driver element.
	button_label
				String. Accomplishment data-control-name value.
	
	'''


	print ('Clicking accomplishment button: ' + str(button_label))
	button_xpath = "//button[@data-control-name='" + str(button_label) + "']"
	scroll_to_item(browser, button_xpath)
	buttons = browser.find_elements_by_xpath(button_xpath)
	#buttons[0].click()
	button_element = buttons[0]
	browser.execute_script("arguments[0].click();", button_element)

	return
	
def get_extra_interests(browser, url):

	interests_links = [
						url + 'detail/interests/influencers/',
						url + 'detail/interests/companies/',
						url + 'detail/interests/groups/',
						url + 'detail/interests/schools/']
	
	for j in range(0, len(interests_links)):
		browser.get(interests_links[j])
		time.sleep(random.uniform(0.7, 1.1))
		scroll_interets(browser)
		soup = get_the_soup(browser)
		interest_followers = profile_html_handler.get_extra_interests(soup)
		for i in range(0, len(interest_followers[0])):
			print ('Topic: '     + str(interest_followers[0][i].encode('utf-8')))
			print ('Followers: ' + str(interest_followers[1][i].encode('utf-8')))
			print ('')
	scroll_interets(browser)
	return

def scroll_interets(browser):

	old_amount = 0
	new_amount = 1
	
	try:
		while old_amount != new_amount:
			time.sleep(random.uniform(0.3, 0.7))
			old_amount = new_amount
			interest_elements = browser.find_elements_by_xpath("//li[@class=' entity-list-item']")
			new_amount = len(interest_elements)
			if new_amount != old_amount:
				interest_elements[-1].location_once_scrolled_into_view
	except:
		print ('Empty interests block')
		pass
	
	return

def open_received_recommendations(browser):

	#xpath = "/html/body/div[5]/div[4]/div[2]/div/div/div/div[2]/div[1]/div[2]/div[6]/div/section/div/artdeco-tabs/artdeco-tablist/artdeco-tab[1]"
	tabs = browser.find_elements_by_tag_name('artdeco-tab')
	if tabs:
		try:
			#tabs[0].click()
			button_element = tabs[0]
			browser.execute_script("arguments[0].click();", button_element)
			print ('Open received recommendations')
			time.sleep(random.uniform(0.3, 0.5))

			expand_button_xpath = "//button[@class='pv-profile-section__see-more-inline link']"
			expand_buttons = browser.find_elements_by_xpath(expand_button_xpath)
			if expand_buttons:
				for i in range(0, len(expand_buttons)):
					try:
						#expand_buttons[i].click()
						button_element = expand_buttons[i]
						browser.execute_script("arguments[0].click();", button_element)
						time.sleep(random.uniform(0.1, 0.3))
					except NoSuchElementException:
						print ('No more expadable buttons')
						pass
					except ElementNotInteractableException:
						print ('Element no interactable')
						pass
		except NoSuchElementException:
			print ('No tab found')
		except ElementNotInteractableException:
			print ('Tab no clickable')
	return
	
def open_given_recommendations(browser):
	'''Find the given recommendations button and click it'''
	#xpath = "/html/body/div[5]/div[4]/div[2]/div/div/div/div[2]/div[1]/div[2]/div[6]/div/section/div/artdeco-tabs/artdeco-tablist/artdeco-tab[2]"
	
	tabs = browser.find_elements_by_tag_name('artdeco-tab')
	if tabs:
		try:
			#tabs[1].click()
			button_element = tabs[1]
			browser.execute_script("arguments[0].click();", button_element)
			print ('Open given recommendations')
			time.sleep(random.uniform(0.3, 0.5))

			expand_button_xpath = "//button[@class='pv-profile-section__see-more-inline link']"
			expand_buttons = browser.find_elements_by_xpath(expand_button_xpath)
			if expand_buttons:
				for i in range(0, len(expand_buttons)):
					try:
						#expand_buttons[i].click()
						button_element = expand_buttons[i]
						browser.execute_script("arguments[0].click();", button_element)
						time.sleep(random.uniform(0.1, 0.3))
					except NoSuchElementException:
						print ('No more expadable buttons')
						pass
					except ElementNotInteractableException:
						print ('Element no interactable')
						pass	
		except NoSuchElementException:
			print ('No tab found')
		except ElementNotInteractableException:
			print ('Tab no clickable')
	return
	
def get_the_soup(browser):
	'''Get the html of the given link. Recieves the browser and a url. Opens the url on the browser and extracts the html.

	Parameters
	----------
	browser
				Driver element
	
	Returns
	-------
	html element
				Contents the current open web page html.
    '''		
	soup = BeautifulSoup(browser.page_source, 'lxml')
	return soup

def save_the_soup(soup, file_name):
	'''Saves the string pased as a first argument on to the local folder debugging_data with the desired name.
	
	Parameters
	----------
	soup
				This is the string to be saved.
				
	file_name
				This is the name of the desired file.
	'''


	cwd = os.getcwd()
	if sys.platform == 'win32':
		directory = str(cwd) + r'\debugging_data\\'
	else:
		directory = str(cwd) + r'/debugging_data/'
	if not os.path.exists(directory):
		os.makedirs(directory)
	
	path = directory + str(file_name) + '.html'
	f = open(path, 'w')
	f.write(str(soup.encode('utf-8', 'ignore')))
	f.close()
	print ('html save in: ' + str(path))
	return
	
if __name__=="__main__":

	url = [ 'https://www.linkedin.com/in/mrogati/',
			'https://www.linkedin.com/in/paul-edlund-998479/',
			'https://www.linkedin.com/in/williamhgates/',
			'https://www.linkedin.com/in/jenna-bromberg-1401a0128/',
			'https://www.linkedin.com/in/taylor-kennedy-49063820',
			'https://www.linkedin.com/in/alicia-hawkins-4740912/',
			'https://www.linkedin.com/in/aliciacostalagomeruelo/',
			'https://www.linkedin.com/in/danielgoleman/',]

	capacity_urls = ['https://www.linkedin.com/in/paul-edlund-998479/',
					 'https://www.linkedin.com/in/james-wetzold-a489035a/',
					 'https://www.linkedin.com/in/paul-woods-02b4274/',
					 'https://www.linkedin.com/in/pallenembark/',
					 'https://www.linkedin.com/in/jorisschut/',
					 'https://www.linkedin.com/in/jasmine-sanie-cpa-31a9b072/',
					 'https://www.linkedin.com/in/george-williams-cfe-cpa-43790448/',
					 ]
			
	browser = open_browser()
	logeate(browser)
	
	## Open profile block
	link = url[-1]
	browser.get(link)
	time.sleep(random.uniform(0.5, 1.3))
	#expand_header(browser)
	#time.sleep(random.uniform(0.5, 0.7))
	#expand_other_links(browser)
	#time.sleep(random.uniform(0.5, 0.7))
	#scroll_to_bottom(browser)
	#expand_all(browser)
	#expand_skills(browser)
	#get_extra_interests(browser, link)
	#expand_all_accomplishments(browser)
	#sopita = get_the_soup(browser)
	#save_the_soup(sopita, 'aliciacostalagomeruelo')
	#for i in range(0, len(url)):
	#	web_html = get_the_soup(browser, str(url[i]))
	#	print web_html
	#time.sleep(random.uniform(0.3, 0.7))
	#web_html = get_the_soup(browser)
	#open_received_recommendations(browser)
	#time.sleep(random.uniform(0.3, 0.7))
	#web_html = get_the_soup(browser)
	#open_given_recommendations(browser)
	#time.sleep(random.uniform(0.3, 0.7))
	#web_html = get_the_soup(browser)
	#accompplish_buttons = profile_html_handler.get_accomplishment_button_names(web_html)
	#for i in range(0, len(accompplish_buttons)):
	#	if accompplish_buttons[i] == 'accomplishments_expand_publications':
	#		click_that_accomplishment_button(browser, accompplish_buttons[i])
	#		time.sleep(random.uniform(0.4, 0.9))
	#		expand_all(browser)
	#		web_html = get_the_soup(browser)
	#		#publication_data = profile_html_handler.get_publications_data(web_html)
	#	if accompplish_buttons[i] == 'accomplishments_expand_certifications':	
	#		click_that_accomplishment_button(browser, accompplish_buttons[i])
	#		time.sleep(random.uniform(0.3, 0.7))
	#		expand_all(browser)
	#		web_html = get_the_soup(browser)
	#		# Call the function to get the data
	#	if accompplish_buttons[i] == 'accomplishments_expand_honors':	
	#		click_that_accomplishment_button(browser, accompplish_buttons[i])
	#		time.sleep(random.uniform(0.3, 0.7))
	#		expand_all(browser)
	#		web_html = get_the_soup(browser)
	#		# Call the function to get the data
	#	if accompplish_buttons[i] == 'accomplishments_expand_languages':	
	#		click_that_accomplishment_button(browser, accompplish_buttons[i])
	#		time.sleep(random.uniform(0.3, 0.7))
	#		expand_all(browser)
	#		web_html = get_the_soup(browser)
	#		# Call the function to get the data
	#	if accompplish_buttons[i] == 'accomplishments_expand_organizations':	
	#		click_that_accomplishment_button(browser, accompplish_buttons[i])
	#		time.sleep(random.uniform(0.3, 0.7))
	#		expand_all(browser)
	#		web_html = get_the_soup(browser)
	#		# Call the function to get the data
	## Open artilces
	#articles_link = link + 'detail/recent-activity/posts/'
	#browser.get(articles_link)
	#time.sleep(random.uniform(0.3, 0.6))
	#scroll_to_bottom(browser)
	## Open posts
	posts_link = link + 'detail/recent-activity/shares/'
	browser.get(posts_link)
	time.sleep(random.uniform(0.3, 0.6))
	scroll_to_bottom(browser)
	

	
	#browser.quit()