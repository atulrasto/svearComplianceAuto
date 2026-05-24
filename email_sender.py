"""Email generated documents through Gmail SMTP."""

import os
import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
from typing import Iterable, Tuple

from config import GMAIL_PASSWORD_ENV_VAR, GMAIL_SMTP_PORT, GMAIL_SMTP_SERVER


def send_email_with_attachments(
    sender_email: str,
    recipient_email: str,
    subject: str,
    body: str,
    attachment_paths: Iterable[Path],
) -> Tuple[bool, str]:
    """Send email with attachments using Gmail SMTP.

    Gmail requires an app password when two-factor authentication is enabled.
    The password is read from the GMAIL_APP_PASSWORD environment variable,
    which can be supplied through the local .env file.
    """
    password = os.getenv(GMAIL_PASSWORD_ENV_VAR)
    if not password:
        return (
            False,
            f"Missing Gmail password. Set environment variable {GMAIL_PASSWORD_ENV_VAR}.",
        )

    if not sender_email or not recipient_email:
        return False, "Sender and recipient email addresses are required."

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = recipient_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    try:
        for path in attachment_paths:
            file_path = Path(path)
            if not file_path.exists():
                return False, f"Attachment not found: {file_path}"

            with file_path.open("rb") as file_obj:
                attachment = MIMEApplication(file_obj.read(), _subtype="docx")

            attachment.add_header(
                "Content-Disposition",
                "attachment",
                filename=file_path.name,
            )
            message.attach(attachment)

        with smtplib.SMTP(GMAIL_SMTP_SERVER, GMAIL_SMTP_PORT, timeout=30) as server:
            server.starttls()
            server.login(sender_email, password)
            server.send_message(message)

        return True, "Email sent successfully."

    except smtplib.SMTPAuthenticationError:
        return False, "Gmail authentication failed. Check your email and app password."
    except smtplib.SMTPException as exc:
        return False, f"SMTP error: {exc}"
    except OSError as exc:
        return False, f"File or network error: {exc}"
