import email
import smtplib
import imaplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import dotenv_values


class Gmail:

    def __init__(self, login, password, smtp="smtp.gmail.com", imap="imap.gmail.com"):
        self.login = login
        self.password = password
        self.smtp = smtp
        self.imap = imap

    def send_message(self, recipients: list, subject: str, text: str):
        massage = MIMEMultipart()
        massage['From'] = self.login
        massage['To'] = ', '.join(recipients)
        massage['Subject'] = subject
        massage.attach(MIMEText(text))
        mail_sender = smtplib.SMTP(self.smtp, 587)
        mail_sender.ehlo()
        mail_sender.starttls()
        mail_sender.ehlo()
        mail_sender.login(self.login, self.password)
        mail_sender.sendmail(self.login, recipients, massage.as_string())
        mail_sender.quit()

    def recieve_mail(self, header=None):
        mail = imaplib.IMAP4_SSL(self.imap)
        mail.login(self.login, self.password)
        mail.list()
        mail.select("Inbox")
        header_option = '(HEADER Subject "%s")' % header if header else 'ALL'
        result, data = mail.uid('search', header_option)
        assert data[0], 'There are no letters with current header'
        latest_email_uid = data[0].split()[-1]
        result, data = mail.uid('fetch', latest_email_uid, '(RFC822)')
        raw_email = data[0][1]
        email_message = email.message_from_bytes(raw_email, policy=email.policy.default)
        mail.logout()
        return email_message


if __name__ == '__main__':
    list_of_recipients = ['support@netology.ru']
    mail = Gmail(dotenv_values('.env')["LOGIN"], dotenv_values('.env')["PASSWORD"])
    mail.send_message(recipients=list_of_recipients, subject="test", text="test")
    mail.recieve_mail()

