import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.mime.text import MIMEText
from email.utils import formataddr


def send(smtp_dict, mail_dict):
    """
    Send mail using SMTP configurations.

    :param smtp_dict: A dictionary with the following keys:
        - ip: The IP of the SMTP server.
        - port: The port of the SMTP server.
        - username: The username of the SMTP account.
        - password: The password of the SMTP account.
        - sender_mail: The email address of the sender.
        - sender_title: The title of the sender account.
        - is_ssl: Boolean to indicate if an SSL is used or not.

    :param mail_dict: A dictionary with the following keys:
        - subject: The subject of the mail.
        - recipients: A list of the email addresses of the receivers.
        - cc: A list of the email addresses in the CC.
        - attachments: A list of the paths of the attachments.
        - message: The message to be sent.

    :return: None
    """

    # Create message
    msg = MIMEMultipart()

    # Set the subject of the mail
    msg['Subject'] = Header(mail_dict['subject'], 'utf-8')

    # Set the sender mail
    msg['From'] = formataddr((
        str(Header(mail_dict['subject'], 'utf-8')),
        smtp_dict['sender_mail']
    ))

    # Send the recipients
    msg['To'] = ', '.join(mail_dict['recipients'])

    # Set the CCs
    msg['Cc'] = ', '.join(mail_dict['cc'])

    # Set the HTML message body
    body = MIMEMultipart('alternative')
    body.attach(MIMEText(mail_dict['message'], 'html'))
    msg.attach(body)

    # Set the attachments
    for file in mail_dict['attachments']:
        with open(file, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
        # Encode file in ASCII characters to send by email
        encoders.encode_base64(part)
        # Add header as key/value pair to attachment part
        part.add_header(
            "Content-Disposition",
            f"attachment; filename= {file}",
        )
        msg.attach(part)

    # Create SMTP object for the SMTP server
    if smtp_dict['is_ssl']:
        server = smtplib.SMTP_SSL(smtp_dict['ip'], smtp_dict['port'])
    else:
        server = smtplib.SMTP(smtp_dict['ip'], smtp_dict['port'])

    # Login to the SMTP server if the username and password are provided
    if smtp_dict['username'] and smtp_dict['password']:
        server.login(smtp_dict['sender_mail'], str(smtp_dict['password']))

    # Send the mail
    server.sendmail(
        smtp_dict['sender_mail'],
        mail_dict['recipients'] + mail_dict['cc'],
        msg.as_string()
    )

    # Quit the server
    server.quit()
