import os
import yaml
from packages.project import project
from packages.mail import mail


def main():

    # Import configurations
    config_path = os.path.join(project.get_absolute_path(), 'config.yaml')
    with open(config_path) as config_file:
        config = yaml.safe_load(config_file)

    # Read the mail HTML template
    mail_template_path = os.path.join(
        project.get_absolute_path(), 'data/input/mail_template.html'
    )
    with open(mail_template_path, "r", encoding='utf-8') as f:
        mail_body = f.read()

    smtp_dict = {
        'ip': config['smtp']['ip'],
        'port': config['smtp']['port'],
        'username': config['smtp']['username'],
        'password': config['smtp']['password'],
        'sender_mail': config['smtp']['sender_mail'],
        'sender_title': config['smtp']['sender_title'],
        'is_ssl': config['smtp']['is_ssl'],
    }

    mail_dict = {
        'subject': "Test Report",
        'recipients': ['muhammadabdelgawwad@gmail.com', ],
        'cc': ['muhammadabdelgawwad@gmail.com', ],
        'attachments': [],
        'message': mail_body,
    }

    mail.send(smtp_dict, mail_dict)


if __name__ == '__main__':
    main()
