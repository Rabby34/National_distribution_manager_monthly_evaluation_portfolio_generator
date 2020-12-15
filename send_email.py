import pic_adder

import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import set_name as mail_info
To_mail=mail_info.to_mail()
Cc_mail=mail_info.cc_mail()

# ------------ Group email ----------------------------------------
msgRoot = MIMEMultipart('related')
me = 'erp-bi.service@gmail.com'            # give from mail
to = To_mail
cc = Cc_mail
bcc = ['', '']

recipient = to + cc + bcc

subject = "NSM Wise Monthly Evaluation Report - SK+F"

email_server_host = ''                 # give server mail
port = 25

msgRoot['From'] = me

msgRoot['To'] = ', '.join(to)
msgRoot['Cc'] = ', '.join(cc)
msgRoot['Bcc'] = ', '.join(bcc)
msgRoot['Subject'] = subject

msgAlternative = MIMEMultipart('alternative')
msgRoot.attach(msgAlternative)

msgText = MIMEText('This is the alternative plain text message.')
msgAlternative.attach(msgText)

msgText = MIMEText("""
                       <img src="cid:report" height='2790', width='1270'><br>

                       """, 'html')

msgAlternative.attach(msgText)

# --------- Set Credit image in mail   -----------------------
fp = open('./images/final_photo.png', 'rb')
report = MIMEImage(fp.read())
fp.close()

report.add_header('Content-ID', '<report>')
msgRoot.attach(report)

# # ----------- Finally send mail and close server connection ---
print('-----------------------------------------------')
print('sending mail')
server = smtplib.SMTP(email_server_host, port)
server.ehlo()
server.sendmail(me, recipient, msgRoot.as_string())
server.close()
print('mail sent')
print('-----------------------------------------------')
