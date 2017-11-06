#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

import smtplib
from smtplib import SMTP
import datetime
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders
import logging

def send_email(f_path, title, message, to_addr):
    '''
    This function connects to a server, build an email, and sends the email.
    
	Parameters
	----------
    f_path  
			Full path of the file.
    title   
			Email title.
    message  
			Screen output of the simulation.
			
	to_addr
			Email recipient.
    '''

    logging.basicConfig(filename='linkedin_crawler.log', format='%(asctime)s - %(filename)s - %(funcName)s - %(levelname)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)
    logger = logging.getLogger('Linkedin_logger')
	
    logger.info('Emailing has been called')
	
    from_addr = "Javi <no-reply@capacity.net>"

    msg = MIMEMultipart()    
    
    msg['From'] = from_addr
    msg['To'] = to_addr
    msg['Subject'] = title

    msg.attach(MIMEText(message, 'plain'))
    
	# Create name for file
    if sys.platform == 'win32':
        path_braken = f_path.split('\\')
    else:
        path_braken = f_path.split('/')
    filename = str(path_braken[-1])
    attachment = open(f_path, "rb")
    
    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
    msg.attach(part)

    logger.info('%s has been attached', f_path)
	
    date = datetime.datetime.now().strftime( "%d/%m/%Y %H:%M" )

    smtp = SMTP()
    server = smtplib.SMTP()
    print "Defined server"
    # Connect to server    
    server.connect("email-smtp.us-west-2.amazonaws.com",25)
    print "Connected"
	# identify ourselves to smtp gmail client
    server.ehlo()
    # secure our email with tls encryption
    server.starttls()
    # re-identify ourselves as an encrypted connection
    server.ehlo()
    print "Complete Initiation"
    server.login('AKIAJOC3IPEHADEG3SJQ', 'AmA5rVttk4UbVavp3m9mUSjkndOEnGUGvvSo8+bMwSmX')
    text = msg.as_string()
    print "Sending mail..."
    server.sendmail(from_addr, to_addr, text)
    server.quit()
    print "Email sent"

    logger.info('Email has been sent to: %s', to_addr)

if __name__=='__main__':
    
	to_addr = "javierpascualr@gmail.com"
	f_path = r'C:\Users\Javier\Desktop\Capacity\Linkedin_DB\linkedin_crawler.log'
	title = 'Hello!!'
	message = 'I have miss you.\nWhere have you been??'
	
	send_email(f_path, title, message, to_addr)
