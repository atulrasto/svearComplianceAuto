# SVEAR Compliance Agent

Local Streamlit web app for generating editable `.docx` compliance documents for **SVEAR FOUNDATION** under the Societies Registration Act, 1860.

The app can generate meeting notices, agendas, attendance sheets, minutes, and resolutions, save them into dated folders, maintain a SQLite log, show compliance reminders, and optionally email the generated document through Gmail SMTP.

## Features

- Streamlit local web interface.
- Editable `.docx` generation using `python-docx`.
- Folder output format: `generated_documents/YYYY/Meeting_Type_Date/`.
- SQLite document log with document type, generation date, meeting date, file path, and email status.
- Gmail SMTP email attachment support.
- Download button for each generated document.
- Compliance reminders for Governing Body meetings, AGM, audit, and election.
- Default sample data for SVEAR Foundation.

## Project Files

- `app.py` - Streamlit interface.
- `document_generator.py` - DOCX document creation and formatting.
- `email_sender.py` - Gmail SMTP attachment sender.
- `database.py` - SQLite log helpers.
- `compliance_calendar.py` - reminder calculations.
- `config.py` - society details, document types, and constants.
- `requirements.txt` - Python dependencies.
- `.env` - local email settings and Gmail app password placeholder.
- `README.md` - setup and usage instructions.

## Setup

Use Python 3.10 or newer. This project was prepared with Python 3.10.11.

```powershell
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If the virtual environment does not exist, create it first:

```powershell
py -3.10 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Run

```powershell
streamlit run app.py
```

Then open the local URL shown by Streamlit, usually:

```text
http://localhost:8501
```

## Environment File

Email settings are stored in `.env` for local use:

```text
GMAIL_SMTP_SERVER=smtp.gmail.com
GMAIL_SMTP_PORT=587
GMAIL_SENDER_EMAIL=your_email@gmail.com
GMAIL_APP_PASSWORD=your_gmail_app_password
DEFAULT_RECIPIENT_EMAIL=
EMAIL_SUBJECT_PREFIX=SVEAR FOUNDATION
```

Update these values before sending email. Keep `.env` private and do not commit it to Git.

## Gmail Email Setup

The app uses Gmail SMTP and does not require paid APIs.

Create a Gmail app password from your Google account security settings, then place it in `.env`:

```text
GMAIL_APP_PASSWORD=your_gmail_app_password
```

Do not hardcode Gmail passwords in the source code.

## Output

Generated documents are saved under:

```text
generated_documents/YYYY/Meeting_Type_Date/
```

The SQLite log is saved as:

```text
svear_compliance.db
```

## Notes

- Documents are generated in professional Indian NGO-style language.
- Generated files are editable Word documents.
- Print and sign documents physically where required.
- Review legal and statutory filings with a qualified professional before submission to any authority.
