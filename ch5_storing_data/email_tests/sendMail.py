import smtplib
from email.mime.text import MIMEText

gmail_user = 'almyko92@gmail.com'
pwFile = open("pw.key", "r")
gmail_pw = pwFile.readline().strip()
pwFile.close()

def sendMail(receiver, subject, body):
    global gmail_user, gmail_pw
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = gmail_user
    msg['To'] = receiver

    try:
        s = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        s.ehlo_or_helo_if_needed()
        s.login(gmail_user, gmail_pw)
        s.send_message(msg)
        s.quit()
        print("Email sent!")
    except smtplib.SMTPAuthenticationError:
        print("Auth Error")
    except smtplib.SMTPSenderRefused:
        print("Sender Refused")
    except smtplib.SMTPResponseException:
        print(smtplib.SMTPResponseException.smtp_error)
    except:
        print("Something went wrong...")

receiver = input("To: ").strip()
subject = input("Subject: ").strip()
body = input("Msg: ").strip()

sendMail(receiver, subject, body)
