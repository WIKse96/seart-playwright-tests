import os
import smtplib
import urllib.request
from email.mime.text import MIMEText


def send_email_notification(subject: str, body: str) -> None:
    sender = os.environ["NOTIFY_EMAIL_FROM"]
    app_password = os.environ["NOTIFY_EMAIL_APP_PASSWORD"]
    recipient = os.environ.get("NOTIFY_EMAIL_TO", sender)

    message = MIMEText(body)
    message["Subject"] = subject
    message["From"] = sender
    message["To"] = recipient

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender, app_password)
        server.sendmail(sender, [recipient], message.as_string())


def send_ntfy_notification(subject: str, body: str) -> None:
    topic = os.environ["NOTIFY_NTFY_TOPIC"]
    server = os.environ.get("NOTIFY_NTFY_SERVER", "https://ntfy.sh")

    request = urllib.request.Request(
        url=f"{server}/{topic}",
        data=body.encode("utf-8"),
        headers={"Title": subject},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=10):
        pass
