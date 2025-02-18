from threading import Thread
from flask import current_app, render_template
from flask_mail import Message
from application.extensions import mail


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(to: str, subject: str, template: str, sender=send_async_email, **kwargs):
    app = current_app._get_current_object()

    app_name = current_app.config["APP_NAME"]
    main_username = current_app.config["MAIL_USERNAME"]

    mail_sender = f"{app_name} <{main_username}>"
    mail_subject_prefix = f"[{app_name}]"

    msg = Message(mail_subject_prefix + " " + subject, sender=mail_sender, recipients=[to])
    msg.html = render_template("emails/" + template + ".html", **kwargs)
    thr = Thread(target=sender, args=[app, msg])
    thr.start()
    return thr
