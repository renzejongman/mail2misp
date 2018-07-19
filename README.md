# Mail to MISP
Email events straight into your MISP. Mail2misp will even parse the IOCs out for you automatically.

Mail to MISP (mail2misp) lets you monitor the inbox of a given email address. Just forward an interesting email, or copy from a blog in an email to your monitored address, and it will ingest it automatically in your MISP instance. You are effectively emailing events straight into MISP.
mail2misp.py will look for unread emails and checks them for Indicators of Compromise (IOCs). If it finds any, a new event in MISP will be created, with the title being the subject of the email and the IOCs as attributes of the event.

### Installation
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


