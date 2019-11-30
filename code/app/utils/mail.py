
# -*- coding: utf-8 -*-

"""Script to send mails."""

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import smtplib


class Mail():
    """Send mails templates to a user."""

    def __init__(self, username, password, server, port):
        """Instance to class."""
        self.username = username
        self.password = password
        self.server = server
        self.port = port

    def send_email(self, from_, to, subject, body, datas, cc=''):
        """Send mail templato to a user by a server."""
        msg = MIMEMultipart()
        msg['From'] = from_
        msg['To'] = to
        msg['Cc'] = cc
        msg['Subject'] = subject
        msg.attach(MIMEText(body, "html"))

        for data in datas:
            if data is not None:
                for _, info in data['images'].items():
                    if info[1] is not None:
                        with open(info[1], 'rb') as fp:
                            msgImage = MIMEImage(fp.read())
                            msgImage.add_header('Content-ID', f'<{info[1]}>')
                            msg.attach(msgImage)

        smtp = smtplib.SMTP(self.server, self.port)
        smtp.starttls()
        smtp.login(self.username, self.password)
        print(smtp.sendmail(from_, [to, cc], msg.as_string()))
        smtp.quit()

    def content(self, datas):
        """Build a template mail body and subject."""
        subject = "TCC - MLaaS Topzero D+"

        body = f"""
            <h1>TCC MLaaS</h1>
            <p>Realizamos o treinamento da base de dados que nos foi enviada. Abaixo você pode ver nossa o resultado dos treinos realizados.</p>
            """

        for data in datas:
            if data is not None:
                for key, info in data['images'].items():
                    body += f"""{info[0]}"""
                    if info[1] is not None:
                        body += f"""<br><img src="cid:{info[1]}" alt="{key}" height="300" width="300"><br>"""

        body += f"""
            </br>
            Atenciosamente
            <h4><b>IESB</b></h4>
            <h5>created by <b>Allan Kleitson Teotonio</b></h5>
            <h5>Science Computer. 2019</h5>
            """

        return subject, body
