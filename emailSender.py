# Import smtplib for the actual sending function
import smtplib
import acorns as sa
# Here are the email package modules we'll need
from email.mime.text import MIMEText

from email.mime.multipart import MIMEMultipart

COMMASPACE = ', '

# Create the container (outer) email message.
def sendEmail(recips=["pauliankline@gmail.com"],sub="Error in music logger",bod="This is the default body."):
    try:
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
        s.login('kjhkmusiclogger@gmail.com', sa.secrets['kj'])
        s.sendmail(me, family, msg.as_string())
        s.quit()# Import smtplib for the actual sending function
    except:
        e_email =str(sys.exc_info()[0])
        v_email = str(sys.exc_info()[1])
        t_email = str(tb.extract_tb(sys.exc_info()[2]))
        error_email = "ERROR:\n" + e_email + "\n\nVALUE:\n" + v_email + "\n\nTRACEBACK:\n" + t_email 
        print(error_email)    
