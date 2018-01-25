import sys

try:
    from django.db import models
    from django.contrib.postgres.fields import ArrayField
except  Exception as e:
    print (e)
    print("There was an error loading django modules. Do you have django installed?")
    sys.exit()

# ExternalEmployee model
class ExternalEmployee(models.Model):

	## Columns from new crawler model
    # The LinkedIn URL. Needed for compatibility
    url                          =            models.CharField(unique=True, max_length=400)
    # Candidate's names as in Linkedin profile. Needed for compatibility
    name                         =            models.CharField(max_length=100)
    # either 2 or 3. 2 means internal (registered) user profiles, 3 means external (from LinkedIn) user profiles.
    source                       =            models.CharField(max_length=100)
    # This is the first job title of a person's current job. Needed for compatibility
    job_title                    =            models.TextField(blank=True, null=True)
    # This is the first job title of a person BEFORE his current job
    job_title_prev               =            models.TextField(blank=True, null=True)
    # But I think for every external profile, company_id is NULL
    company_id                   =            models.IntegerField(blank=True, null=True)
    capacity_rate                =            models.FloatField(blank=True, null=True)
	# first location that can be extracted from a person's experience for his current job. Needed for compatibility
    location                     = ArrayField(models.CharField(max_length=100), blank=True, null=True)
	# the first location that can be extracted from a person's experience panel without the current job
    location_prev                =            models.CharField(max_length=100 , blank=True, null=True)
    # skills extracted from panel "Featured Skills & Endorsements". Needed for compatibility
    skills                       = ArrayField(models.CharField(max_length=100), blank=True, null=True)
    # number of endorsements extracted from the panel "Featured Skills & Endorsements". Needed for compatibility
    endorsements                 = ArrayField(models.IntegerField(), blank=True, null=True)
    # working experience in years. Needed for compatibility
    experience                   =            models.IntegerField(blank=True, null=True)
    # timestamp type in postgresql. Needed for compatibility
    date_created                 =            models.DateTimeField(editable=False)
    date_updated                 =            models.DateTimeField(blank=True, null=True)
    # date when the most recent job started. Needed for compatibility
    job_started                  =            models.CharField(max_length=500 , blank=True, null=True)
    # It indicates all the starting dates of all current jobs
    ai_current_working_started   = ArrayField(models.CharField(max_length=500), blank=True, null=True)
	# indicates all the starting dates of all previous jobs
    ai_previous_working_started  = ArrayField(models.CharField(max_length=500), blank=True, null=True)
    #  indicates all the finishing dates of all previous jobs
    ai_previous_working_finished = ArrayField(models.CharField(max_length=500), blank=True, null=True)
    # all the job titles of all current jobs
    ai_current_job_title         = ArrayField(models.CharField(max_length=500), blank=True, null=True)
    # all the job titles of all previous jobs
    ai_previous_job_title        = ArrayField(models.CharField(max_length=500), blank=True, null=True)
    # all the company names of all current jobs
    ai_current_company           = ArrayField(models.CharField(max_length=500), blank=True, null=True)
    # all the company names of all previous jobs
    ai_previous_company          = ArrayField(models.CharField(max_length=500), blank=True, null=True)
    # all the locations of all current jobs
    ai_current_locations         = ArrayField(models.CharField(max_length=500), blank=True, null=True)
    # all the locations of all previous jobs
    ai_previous_locations        = ArrayField(models.CharField(max_length=500), blank=True, null=True)
    # current working contents of a person's current job, extracted from Experience panel. 
    # If a person has several current jobs, they should be separated by "+-+-+-+-+-". Needed for compatibility
    current_working_content      =            models.TextField(blank=True, null=True)
    # previous working content descriptions of a person's previous jobs, extracted from Experience panel. Needed for compatibility
    previous_working_content     =            models.TextField(blank=True, null=True)
    # company extracted from first current working experience in Experience panel. Needed for compatibility
    company                      =            models.CharField(max_length=500 , blank=True, null=True)
    # interests extracted from Interests panel, which are related to the current company.
    ai_interests_current_related = ArrayField(models.CharField(max_length=500), blank=True, null=True)
    # interests extracted from Interests panel, which are not related to the current company. Needed for compatibility
    interests                    = ArrayField(models.CharField(max_length=500), blank=True, null=True)
    # This is the school name where a person acquires her/his highest degree.
    ai_education                 =            models.CharField(max_length=500 , blank=True, null=True)
    # school names where a person attends before. Needed for compatibility
    previous_education           = ArrayField(models.CharField(max_length=500), blank=True, null=True)
	# highest degree of a person. Needed for compatibility
    degree                       =            models.CharField(max_length=500 , blank=True, null=True)
	# degree of a person excluding his highest degree appears in ai_degree column
    ai_previous_degree           = ArrayField(models.CharField(max_length=500), blank=True, null=True)
	# education field of a person where s/he acquired her/his highest degree. Needed for compatibility
    education_field              =            models.CharField(max_length=500 , blank=True, null=True)
	#  this is all the information as shown on the top education in the education block. Needed for compatibility
    education                    =            models.TextField(blank=True, null=True)
    # education field of a person s/he acquired excluding her/his highest degree
    ai_previous_education_field  = ArrayField(models.CharField(max_length=500), blank=True, null=True)
    # starting year of a person's ALL studies.
    ai_education_start           = ArrayField(models.CharField(max_length=500), blank=True, null=True)
    # finishing year of a person's ALL studies.
    ai_education_finished        = ArrayField(models.CharField(max_length=500), blank=True, null=True)
    # information extracted from self introduction panel. Needed for compatibility
    self_intro                   =            models.TextField(blank=True, null=True)
    # information extracted from the Volunteer Experience panel. Needed for compatibility
    volunteer_experience         =            models.TextField(blank=True, null=True)
    #  extracted from the Recommendations panel
    recommendation_given         =            models.TextField(blank=True, null=True)
    #  extracted from the Recommendations panel
    recommendation_received      =            models.TextField(blank=True, null=True)
    # 
    ai_activity_articles         =            models.TextField(blank=True, null=True)
    ai_activity_posts            =            models.TextField(blank=True, null=True)
    ai_activity_liked            =            models.TextField(blank=True, null=True)
    # Followers from activity page
    activity_followers           =            models.IntegerField(blank=True, null=True)
    # From accomplishment language panel
    accomplishment_language      = ArrayField(models.CharField(max_length=500), blank=True, null=True)
    # From accomplishment course panel
    accomplishment_course        =            models.TextField(blank=True, null=True)
    # From accomplishment project panel
    accomplishment_project       =            models.TextField(blank=True, null=True)
    # From accomplishment certification panel
    accomplishment_certification =            models.TextField(blank=True, null=True)
    # From accomplishment organizations panel
    accomplishment_organization  =            models.TextField(blank=True, null=True)
    # From accomplishment honor panel
    accomplishment_honor         =            models.TextField(blank=True, null=True)
    # From accomplishment publication panel
    accomplishment_publication   =            models.TextField(blank=True, null=True)
    # From accomplishment patent panel
    accomplishment_patent        =            models.TextField(blank=True, null=True)
    # From accomplishment scorer panel
    accomplishment_scorer        =            models.TextField(blank=True, null=True)
    # TRUE for all external profiles.
    is_active                    =            models.CharField(max_length=500 , blank=True, null=True)
    # All of the fields below are from the top lines, just under the name
    current_position             =            models.CharField(max_length=500 , blank=True, null=True)
    current_company              =            models.CharField(max_length=500 , blank=True, null=True)
    most_important_certificate   =            models.CharField(max_length=500 , blank=True, null=True)
    most_important_education     =            models.CharField(max_length=500 , blank=True, null=True)
    # links retrieved from other links section
    facebook_link                =            models.CharField(max_length=500 , blank=True, null=True)
    twitter_link                 =            models.CharField(max_length=500 , blank=True, null=True)
    emails                       = ArrayField(models.CharField(max_length=500), blank=True, null=True)
    all_links                    = ArrayField(models.CharField(max_length=500), blank=True, null=True)	

	
	
class Meta:
    managed = False
    db_table = 'external_employee'