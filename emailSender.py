# Import smtplib for the actual sending function
import smtplib

# Here are the email package modules we'll need
from email.mime.text import MIMEText

from email.mime.multipart import MIMEMultipart

COMMASPACE = ', '

# Create the container (outer) email message.
msg = MIMEText("here is the mime text")
msg['Subject'] = 'Error in Music Logger'
me = 'musiclogger@no-reply.com'
family = ['pauliankline@gmail.com']
msg['From'] = me
msg['To'] = COMMASPACE.join(family)
#msg.preamble = 'Our family reunion'
#msg['Body']="hey, this is the body"

# Send the email via our own SMTP server.
s = smtplib.SMTP('localhost')
s.sendmail(me, family, msg.as_string())
s.quit()# Import smtplib for the actual sending function
