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
        'hostname': config['smtp']['hostname'],
        'port': config['smtp']['port'],
        'sender': config['smtp']['sender'],
        'password': config['smtp']['password'],
        'sender_title': config['smtp']['sender_title'],
    }

    mail_dict = {
        'subject': "Database Daily Backup Report",
        'recipients': ['muhammadabdelgawwad@gmail.com', ],
        'cc': ['muhammadabdelgawwad@gmail.com', ],
        'attachments': [],
        'message': mail_body,
    }

    mail.send(smtp_dict, mail_dict)


if __name__ == '__main__':
    main()
