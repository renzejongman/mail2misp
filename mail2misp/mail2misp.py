#!/usr/bin/env python3
## Author: 		Renze Jongman
## Version: 	0.0.1
## Date:		19 July 2018
## Title: 		Mail to MISP
## Description:	monitors a give email address for forwarded messages, scrapes IOCs from them and creates an event in MISP with those IOC.
## 				don't forget to set-up config.py with your email and MISP details.
import logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s\t- %(levelname)s\t- %(message)s", datefmt='%m/%d/%Y %I:%M:%S %p')

from pymisp     import PyMISP
from iocparser 	import IOCParser
from config 	import *
from imapclient	import IMAPClient 
import pyzmail, email


class eMail:
	# instances of this class are single, unread emails from the monitored email account.

	def __init__(self, subject=None, body=None):
		self.subject 	= subject
		self.body 		= body
		self.iocs 		= self.getIOCs()

	def getIOCs(self):
		iocObj = IOCParser(self.body)
		return iocObj.parse()


#Setting up the imap-server and selecting unread emails from the INBOX.
def getEmails():
	global server
	server = IMAPClient(IMAPSERVER, ssl=True)
	logging.info("Connected to {}".format(IMAPSERVER))
	server.login(USERNAME, PASSWORD)
	server.select_folder('INBOX', readonly=False)
	newMails = server.search(criteria = [u'UNSEEN'])
	logging.info("Found {} new messages.".format(len(newMails)))

	logging.info(newMails)

	rawMails = server.fetch(newMails, ['BODY[]'])
	return rawMails


# Grabbing the subject line (for the event title in MISP) and body (for IOC-scraping) from the new emails from the getEmails()-function.
def parseMails(rawMails):
	for uid in rawMails:
		logging.debug("Working on email with UID: #{}".format(uid))
		mail = pyzmail.PyzMessage.factory(rawMails[uid][b'BODY[]'])
		logging.info("found a new email with subject: {}".format(mail.get_subject()))
		subject = mail.get_subject()

		if mail.text_part != None:
			logging.debug("plain text_part present in email")
			body = mail.text_part.get_payload().decode(mail.text_part.charset)
		elif mail.html_part != None:
			logging.debug("no plain text, but html_part present in email. Attempting to scrape from html.")
			body = mail.html_part.get_payload().decode(mail.html_part.charset)
		else:
			logging.warning("Email doesn't have text or html content. Ignoring the email.")
			body = None

		parsedMails.append(eMail(subject=subject, body=body))
	
	logging.info("total number of emails parsed: {}".format(len(parsedMails)))

	return parsedMails


class generateEvents():
    # generates a seperate event for every email with 1 or more parsed IOC, after initialising a connection with the MISP instance.
    # instances of the email class are calles 'pastes' here because the code was borrowed from my pastebin2misp-script.


    def __init__(self, paste):
        self.paste  = paste
        self.url    = MISP_URL
        self.key    = MISP_KEY


    def initMISP(self):
        self.misp   = PyMISP(self.url, self.key, False, 'json', debug=False)

    def addEvents(self):
        for i in range(len(self.paste)):
            if len(self.paste[i].iocs) != 0:
                logging.debug("Paste: {}, # of IOCs: {}. Creating an event.".format(self.paste[i].subject, len(self.paste[i].iocs)))
                event   = self.misp.new_event(distribution=1, analysis=1, info=self.paste[i].subject)


                for j in range(len(self.paste[i].iocs)):
                    if self.paste[i].iocs[j].kind   == "IP":
                        self.misp.add_ipsrc(event, self.paste[i].iocs[j].value)
                    elif self.paste[i].iocs[j].kind == "uri":
                        self.misp.add_url(event, self.paste[i].iocs[j].value)
                    elif self.paste[i].iocs[j].kind == "md5":
                        self.misp.add_hashes(event, md5=self.paste[i].iocs[j].value)
                    elif self.paste[i].iocs[j].kind == "sha1":
                        self.misp.add_hashes(event, sha1=self.paste[i].iocs[j].value)
                    elif self.paste[i].iocs[j].kind == "sha256":
                        self.misp.add_hashes(event, sha256=self.paste[i].iocs[j].value)
                    elif self.paste[i].iocs[j].kind == "CVE":
                        #self.misp.add_object(event, 63, self.paste[i].iocs[j].value)
                        pass
                    if self.paste[i].iocs[j].kind   == "email":
                        self.misp.add_email_src(event, self.paste[i].iocs[j].value)
                    if self.paste[i].iocs[j].kind   == "filename":
                        self.misp.add_filename(event, self.paste[i].iocs[j].value)

                if PUBLISH_EVENTS:
                	self.misp.publish(event, alert=EMAIL_ALERTS)


if __name__ == "__main__":
	newMsgs			= getEmails()
	parsedMails 	= []
	fetchedMails 	= parseMails(newMsgs)
	logging.info(server.get_flags(newMsgs))
	server.set_flags(newMsgs, [b'\\Seen'])
	logging.debug(server.get_flags(newMsgs))
	server.logout()
	
	# Generate events, connect to the MISP-server, and add the events to the MISP-instance:
	x = generateEvents(fetchedMails)
	x.initMISP()
	x.addEvents()
	



