import smtplib
from email.mime.text import MIMEText

gmail_user = 'almyko92@gmail.com'
pwFile = open("pw.key", "r")
gmail_pw = pwFile.readline().strip()
pwFile.close()

msg = MIMEText("The body of the email")

msg['Subject'] = "Python Email Test"
msg['From'] = "almyko92@gmail.com"
msg['To'] = "almyko92@gmail.com"

try:
    s = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    s.ehlo()
    s.login(gmail_user, gmail_pw)
    s.send_message(msg)
    s.quit()
    print("Email sent!")
except:
    print("Something went wrong...")
