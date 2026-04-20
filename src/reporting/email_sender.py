import smtplib
from email.message import EmailMessage
import os


def send_email_report(to_email, subject, body, attachments=None):


    # set EMAIL_USER=tejshree.shinde@infobeans.com
    # set EMAIL_PASSWORD=fbskxutzsnzetntd

    from_email = os.getenv("EMAIL_USER")
    password = os.getenv("EMAIL_PASSWORD")
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = from_email
    msg["To"] = to_email
    msg.set_content(body)

    # Attach files
    for file in attachments or []:
        with open(file, "rb") as f:
            msg.add_attachment(
                f.read(),
                maintype="application",
                subtype="octet-stream",
                filename=os.path.basename(file)
            )

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(from_email, password)
        smtp.send_message(msg)