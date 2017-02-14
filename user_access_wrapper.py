#!/usr/bin/python
import commands, os, sys, fnmatch, smtplib

from email import Encoders
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.MIMEMultipart import MIMEMultipart
from email.Utils import COMMASPACE, formatdate


servers = ['server1', 'server2', 'server3' ]

TO = ['somebody@somedomain.com', 'someoneelse@anotherdomain.com' ]
FROM = 'noreply@domain.com'
SUBJECT = 'OS level access extract'


for server in servers:
  cmd = 'ssh %s python < /home/sys/audit/scripts/user_access.py > %s.txt' %(server, server)
  commands.getoutput(cmd)

#filepath = '/home/sys/audit/scripts'
filepath = '/home/sys/audit'
files = os.listdir(filepath)

attachments = []

for file in files:
  if fnmatch.fnmatch(file, '*.txt'):
    fullpath = filepath + '/' + file
    attachments.append(fullpath)


filePath = attachments


msg = MIMEMultipart()

msg['Subject'] = SUBJECT
msg['From'] = FROM
msg['To'] = ", ".join(TO)
body = 'This email is generated from the script /home/sys/audit/scripts/user_access.py on server sysmgt1-1'

for file in filePath:
    part = MIMEBase('application', "octet-stream")
    part.set_payload( open(file,"rb").read() )
    Encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(file))
    msg.attach(part)

part1 = MIMEText(body, 'plain')
msg.attach(part1)

s=smtplib.SMTP('exmail')
s.sendmail(FROM, TO, msg.as_string())
s.close()

for file in filePath:
  os.remove(file)
