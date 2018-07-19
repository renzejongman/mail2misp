# Mail to MISP
Email events straight into your MISP. Mail2misp will even parse the IOCs out for you automatically.

Mail to MISP (mail2misp) lets you monitor the inbox of a given email address. Just forward an interesting email, or copy from a blog in an email to your monitored address, and it will ingest it automatically in your MISP instance. You are effectively emailing events straight into MISP.
mail2misp.py will look for unread emails and checks them for Indicators of Compromise (IOCs). If it finds any, a new event in MISP will be created, with the title being the subject of the email and the IOCs as attributes of the event.

### Installation
* Set-up a dedicated email-address. For example: `add-event@your-misp-domain.com`
* Clone this repository: `git clone https://github.com/renzejongman/mail2misp`
* Provide your email (IMAP) details and MISP instance details in config.py (more detail below)
* Set up a line in your crontab to run the script regularly. For example:
	* `sudo crontab -e`
	* add the following line (change the path): `0 * * * * /home/your-username/path/to/mail2misp/mail2misp/mail2misp.py` to run it every hour, on the hour.

### config.py
* `IMAPSERVER`		is your email provider's IMAP server. Your ISP will have it listed on its website. For example: `imap.google.com`.
* `USERNAME` 		is your username for the IMAP-server. This is often the email-address that you are monitoring.
* `PASSWORD`		is the password for your email-address. If you are using gmail, you will have to generate and set up a seperate password.
* `MISP_URL`		The FQDN for your misp instance. For example: `https://misp.your-domain.com`
* `MISP_KEY`		You can find your key under your profile in MISP
* `PUBLISH_ALERTS`	Set to True if you want the alerts automatically published. Leave to False if you want to add tags and evaluate first (recommended)
* `EMAIL_ALERTS`	If this one AND `PUBLISH_ALERT` are set to True, members of your organisation will receive an email when the event is published.

### Dependencies
* imapclient:	`python3 -m pip install imapclient`
* iocparser:	`python3 -m pip install iocparser`
* pyzmail:		`python3 -m pip install pyzmail`

### Really good ideas
* sharing is set to 'this community'. Be sure you have permission to share from the source of the intel.
* remove any signature blocks from the email you are about to forward. The urls and email addresses would be recognised as artifacts
* remove (other) links that are not IOCs
* before you publish: review the event for what you've tagged for IDS (virustotal-links for example can be useful, but should not be exported to an IDS rule)
* remove things like FW: and RE: from the subject line.
