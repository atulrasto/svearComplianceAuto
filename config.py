"""Application configuration and default SVEAR Foundation data."""

import os
from pathlib import Path

from dotenv import load_dotenv


APP_NAME = "SVEAR Compliance Agent"

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

GENERATED_DOCUMENTS_DIR = BASE_DIR / "generated_documents"
DATABASE_PATH = BASE_DIR / "svear_compliance.db"


SOCIETY_DETAILS = {
    "name": "SVEAR FOUNDATION",
    "full_form": "Solidarity of Volunteers for Environmental Awareness Revolution",
    "registered_office": "1B, Gautam Nagar, New Delhi - 110049",
    "area_of_operation": "All over India",
    "roles": [
        "President",
        "Vice President",
        "Secretary",
        "Joint Secretary",
        "Treasurer",
        "Executive Members",
    ],
}


DOCUMENT_TYPES = [
    "Governing Body Meeting Notice",
    "Governing Body Meeting Agenda",
    "Governing Body Meeting Attendance Sheet",
    "Governing Body Meeting Minutes",
    "Annual General Meeting Notice",
    "Annual General Meeting Agenda",
    "AGM Minutes",
    "Resolution",
    "Auditor Appointment Resolution",
    "Bank Account Operation Resolution",
    "Membership Approval Resolution",
    "Project Approval Resolution",
]


MEETING_TYPES = [
    "Governing Body Meeting",
    "Annual General Meeting",
    "Emergency Governing Body Meeting",
    "General Body Meeting",
    "Project Committee Meeting",
]


DEFAULT_AGENDA_ITEMS = [
    "To confirm the minutes of the previous meeting.",
    "To review ongoing programmes and compliance status.",
    "To discuss financial matters and annual accounts.",
    "To consider new memberships, projects, or resolutions as applicable.",
    "Any other matter with the permission of the Chair.",
]


DEFAULT_MEMBERS = [
    "Amit Kumar - President",
    "Neha Sharma - Vice President",
    "Rohit Verma - Secretary",
    "Priya Singh - Joint Secretary",
    "Sanjay Mehta - Treasurer",
    "Kavita Rao - Executive Member",
]


COMPLIANCE_RULES = {
    "Normal meeting notice": "15 days",
    "Emergency meeting notice": "24 hours",
    "Governing Body meeting quorum": "1/3 members",
    "General Body meeting quorum": "2/3 members",
    "Governing Body meeting frequency": "At least once every 3 months",
    "AGM": "Once every year",
    "Election": "Every 5 years",
    "Audit": "Annual accounts must be audited every year",
    "Registrar filing": "Annual list of Governing Body should be maintained",
}


GMAIL_SMTP_SERVER = os.getenv("GMAIL_SMTP_SERVER", "smtp.gmail.com")
GMAIL_SMTP_PORT = int(os.getenv("GMAIL_SMTP_PORT", "587"))
GMAIL_SENDER_EMAIL = os.getenv("GMAIL_SENDER_EMAIL", "your_email@gmail.com")
DEFAULT_RECIPIENT_EMAIL = os.getenv("DEFAULT_RECIPIENT_EMAIL", "")
EMAIL_SUBJECT_PREFIX = os.getenv("EMAIL_SUBJECT_PREFIX", SOCIETY_DETAILS["name"])
GMAIL_PASSWORD_ENV_VAR = "GMAIL_APP_PASSWORD"
