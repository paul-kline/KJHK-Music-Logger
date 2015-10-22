# Import smtplib for the actual sending function
import smtplib

# Here are the email package modules we'll need
from email.mime.text import MIMEText

from email.mime.multipart import MIMEMultipart

COMMASPACE = ', '

# Create the container (outer) email message.
def sendEmail(recips=["pauliankline@gmail.com"],sub="Error in music logger",bod="This is the default body."):
    
    msg = MIMEText(bod) #"here is the mime text")
    msg['Subject'] = sub #'Error in Music Logger'
    me = 'kjhkmusiclogger@gmail.com'
    family = recips #['pauliankline@gmail.com']
    msg['From'] = me
    msg['To'] = COMMASPACE.join(family)
    #msg.preamble = 'Our family reunion'
    #msg['Body']="hey, this is the body"

    # Send the email via our own SMTP server.
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login('kjhkmusiclogger@gmail.com','EMAIL')
    s.sendmail(me, family, msg.as_string())
    s.quit()# Import smtplib for the actual sending function
