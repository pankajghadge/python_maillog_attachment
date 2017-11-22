#!/usr/bin/python

import glob, os, time
import smtplib
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate

def find_files_newer_than_x_days(dest_dir, file_name, mtime):
    files=[]
    now = time.time()

    for f in glob.glob(dest_dir+"/"+file_name):
        if os.stat(f).st_mtime > now - mtime * 86400:
            if os.path.isfile(f):
                files.append( f )

    return files

def send_mail(send_from, send_to, subject, text, files=None, server="127.0.0.1"):
    assert isinstance(send_to, list)

    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = COMMASPACE.join(send_to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    msg.attach(MIMEText(text))

    for f in files or []:
        with open(f, "rb") as fil:
            part = MIMEApplication(
                fil.read(),
                Name=basename(f)
            )
        # After the file is closed
        part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
        msg.attach(part)


    smtp = smtplib.SMTP(server)
    smtp.sendmail(send_from, send_to, msg.as_string())
    smtp.close()

mail_from = "no-reply.prd@example.com"
mail_to = ["abc@example.com", "xyz@example.com"]
subject = "Maillog files"
message = "Hi, \n\nPlease find the attached maillog files.\nThis is an automatically generated email - Please do not reply to it :)\n\nThanks"
attachments = find_files_newer_than_x_days('/var/log', 'maillog*', 8)

send_mail(mail_from, mail_to, subject, message, attachments)
