#!/usr/bin/env python3

"""
        FT_Collect_Dashboard_2022

    Author: bricetoffolon
    Created on: 22/06/2022
    About: 

"""

from traceback import print_exc

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from src.core.settings import config
from src.db.models import User

from src.core.settings import config


def send_message(message):
    try:
        sg = SendGridAPIClient(config['API_KEY'])
        sg.send(message)
    except Exception:
        print_exc()


def send_mail(link: str, subject: str, catch_phrase: str, user_email: str):
    f = open('backend/core/mailing/mail_template.html', 'r')

    html_content = f.read().format(title=subject, catch_phrase=catch_phrase, link=f'{config["HOST"]}{link}')

    send_message(
        Mail(
            from_email=config['EMAIL'],
            to_emails=user_email,
            subject=subject,
            html_content=html_content
        )
    )


def send_verification_mail(user: User):
    link: str = f'/user/verified/' + user.validation_token[88:]

    catchphrase: str = 'Bonjour %s, Cliquez sur le lien ci-dessous afin de vérifier votre compte' % user.username

    send_mail(link, "Vérifier votre compte", catchphrase, user.email)


def send_reset_password_mail(user: User):
    link: str = '/user/reset_password/' + user.validation_token[88:]

    catchphrase: str = 'Bonjour %s, Cliquez sur le lien ci-dessous afin de réinitialiser votre mot de passe' % user.username

    send_mail(link, "Réinitialiser votre mot de passe", catchphrase, user.email)
