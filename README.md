# Linkedin_crawler
Linkedin crawler and parser.

The crawler needs of a Linkedin account to work.
The Linkedin account variables are found in Linkedin_crawler/data.py

For the emailing system to work, the email must be set up.
Email data is entered on Linkedin_crawler/inputs/emailing_data.py
Here the first value will be the email receiver, the second value the sender email, and the third the password.
Note that the server used is an amazon server. For another email provider, the server must be changed.
The server is set in Linkedin_crawler/emailing.py

The search values are found in Linkedin_crawler/inputs/titles.py

To run the crawler use the command:
$ python main.py

To see the options run:
$ python main.py --h

The crawler can run with Firefox or PhantomJS. The webdrivers must be downloaded and their paths added to the environment variables.

The data from the profiles can be stored on a database. But its is necessary to create the database before running the crawler.
