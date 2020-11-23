import smtplib, ssl
from flask import current_app
import datetime

import logging
logger = logging.getLogger( __name__ )

def getEmailService():
    if hasattr(current_app, 'emailService') == False:
        raise Exception('EmailService has not been initialized')
    return current_app.emailService

def setEmailService(app, smtpServer: str, smtpPort:int, sender: str, senderEmail: str, smtpPassword: str, templatesPath: str) -> None:
    app.emailService = EmailService(smtpServer, smtpPort, sender, senderEmail, smtpPassword, templatesPath)

class EmailService():
    def __init__(self, smtpServer: str, smtpPort:int, sender: str, senderEmail: str, smtpPassword: str, templatesPath: str):
        self.smtpServer = smtpServer
        self.smtpPort = smtpPort
        self.sender = sender
        self.senderEmail = senderEmail
        self.smtpPassword = smtpPassword
        self.templatesPath = templatesPath

    def sendEmail(self, receiver: str, receiverEmail: str, emailContents: str) -> None:
        context = ssl.create_default_context()
        with smtplib.SMTP(self.smtpServer, self.smtpPort) as server:
            server.starttls(context=context)
            server.login(self.senderEmail, self.smtpPassword)

            headers = {
                'Content-Type': 'text/html; charset=utf-8',
                'Content-Disposition': 'inline',
                'Content-Transfer-Encoding': '8bit',
                'From': self.sender + '<' + self.senderEmail + '>',
                'To': receiver + '<' + receiverEmail + '>',
                'Date': datetime.datetime.now().strftime('%a, %d %b %Y  %H:%M:%S %Z'),
            }

            # create the message
            msg = ''
            for key, value in headers.items():
                msg += "%s: %s\n" % (key, value)

            # add contents
            msg += (emailContents)
            logger.error(msg)

            server.sendmail(self.senderEmail, receiverEmail, msg.encode("utf8"))

    def prepareContents(self, templateName: str, locale: str, **kwargs) -> str:
        filename = '/'.join([self.templatesPath, locale, templateName+'.tpl'])
        with open(filename, 'r', encoding='utf-8') as reader:
            contents = reader.read()
            for key, value in kwargs.items():
                logger.error(key)
                contents = contents.replace('{{'+key+'}}', value)

        return contents
