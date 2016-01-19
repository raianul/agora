from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from mimetypes import guess_type
from email.encoders import encode_base64
from smtplib import SMTP


class Email(object):
    def __init__(self, from_, to, subject, message, message_type='plain',
                 attachments=None, cc=None, message_encoding='utf-8'):

        self.email = MIMEMultipart()
        self.email['From'] = from_
        self.email['To'] = to
        self.email['Subject'] = subject

        if cc is not None:
            self.email['Cc'] = cc
        text = MIMEText(message, message_type, message_encoding)
        self.email.attach(text)

        if attachments is not None:
            for filename, content in attachments.iteritems():
                mimetype, encoding = guess_type(filename)
                mimetype = mimetype.split('/', 1)
                attachment = MIMEBase(mimetype[0], mimetype[1])
                attachment.set_payload(content)
                encode_base64(attachment)
                attachment.add_header(
                    'Content-Disposition',
                    'attachment',
                    filename=filename
                )
                self.email.attach(attachment)

    def __str__(self):
        return self.email.as_string()


class EmailConnection(object):
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.connect_to_gmail()

    def connect_to_gmail(self):
        self.connection = SMTP('smtp.gmail.com', 587)
        self.connection.starttls()
        self.connection.ehlo()
        self.connection.login(self.username, self.password)

    def send(self, message, to=None, subject=None):
        if isinstance(message, basestring):
            if to is None or subject is None:
                raise ValueError('You need to specify both `to` and `subject`')
            else:
                message = Email(
                    from_=self.username,
                    to=to,
                    subject=subject,
                    message=message
                )
        from_ = message.email['From']
        to = message.email['To'].split(',')
        if 'Cc' in message.email:
            to = to + message.email['Cc'].split(',')
        message = str(message)
        self.connection.sendmail(from_, to, message)
        self.connection.close()
