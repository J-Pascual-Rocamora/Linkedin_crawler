#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

import smtplib
from smtplib import SMTP as SMTP 
import datetime
from imaplib import IMAP4
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import logging

from Linkedin_crawler.inputs.emailing_data import emailing_data

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
	
    from_addr = emailing_data[1]

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

    server = smtplib.SMTP()
    print ("Defined server")
    # Connect to server    
    server.connect("email-smtp.us-west-2.amazonaws.com",25)
	# Line below was added for Python3 implementation
    server._host = 'email-smtp.us-west-2.amazonaws.com'
    print ("Connected")
	# identify ourselves to smtp gmail client
    server.ehlo()
    # secure our email with tls encryption
    server.starttls()
    # re-identify ourselves as an encrypted connection
    server.ehlo()
    print ("Complete Initiation")
    server.login(emailing_data[1], emailing_data[2])
    text = msg.as_string()
    print ("Sending mail...")
    server.sendmail(from_addr, to_addr, text)
    server.quit()
    print ("Email sent")

    logger.info('Email has been sent to: %s', to_addr)

if __name__=='__main__':
    
	to_addr = emailing_data[0]
	f_path = file_path
	title = 'Hello!!'
	message = 'I have miss you.\nWhere have you been??'
	
	send_email(f_path, title, message, to_addr)
