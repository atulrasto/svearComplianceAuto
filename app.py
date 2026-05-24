"""Streamlit app for generating SVEAR Foundation compliance documents."""

from datetime import date
from pathlib import Path

import pandas as pd
import streamlit as st

from compliance_calendar import build_compliance_reminders
from config import (
    APP_NAME,
    COMPLIANCE_RULES,
    DEFAULT_AGENDA_ITEMS,
    DEFAULT_MEMBERS,
    DEFAULT_RECIPIENT_EMAIL,
    DOCUMENT_TYPES,
    EMAIL_SUBJECT_PREFIX,
    GMAIL_PASSWORD_ENV_VAR,
    GMAIL_SENDER_EMAIL,
    MEETING_TYPES,
    SOCIETY_DETAILS,
)
from database import add_document_log, fetch_document_logs, init_db, update_email_status
from document_generator import generate_document
from email_sender import send_email_with_attachments


def _split_lines(value: str) -> list[str]:
    """Convert a multiline text box into a clean list."""
    return [line.strip() for line in value.splitlines() if line.strip()]


def _read_file_bytes(file_path: Path) -> bytes:
    with file_path.open("rb") as file_obj:
        return file_obj.read()


def show_header() -> None:
    st.set_page_config(page_title=APP_NAME, layout="wide")
    st.title(APP_NAME)
    st.caption("Local document automation for society meetings, resolutions, filing, and signatures.")

    with st.expander("SVEAR Foundation profile", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Name:** {SOCIETY_DETAILS['name']}")
            st.write(f"**Full Form:** {SOCIETY_DETAILS['full_form']}")
            st.write(f"**Registered Office:** {SOCIETY_DETAILS['registered_office']}")
        with col2:
            st.write(f"**Area of Operation:** {SOCIETY_DETAILS['area_of_operation']}")
            st.write("**Governing Body roles:**")
            st.write(", ".join(SOCIETY_DETAILS["roles"]))


def document_form() -> None:
    st.subheader("Generate Compliance Document")

    with st.form("document_generation_form"):
        col1, col2 = st.columns(2)
        with col1:
            document_type = st.selectbox("Document type", DOCUMENT_TYPES)
            meeting_type = st.selectbox("Meeting type", MEETING_TYPES)
            meeting_date = st.date_input("Meeting date", value=date.today())
            meeting_time = st.text_input("Meeting time", value="11:00 AM")
            venue = st.text_input("Venue", value=SOCIETY_DETAILS["registered_office"])
        with col2:
            chairperson_name = st.text_input("Chairperson name", value="Amit Kumar")
            secretary_name = st.text_input("Secretary name", value="Rohit Verma")
            resolution_subject = st.text_input(
                "Resolution subject",
                value="Approval of compliance and administrative matter",
            )
            send_email = st.checkbox("Email generated document for signature", value=False)
            sender_email = st.text_input("Gmail sender", value=GMAIL_SENDER_EMAIL)
            recipient_email = st.text_input("Recipient email", value=DEFAULT_RECIPIENT_EMAIL)

        agenda_items_text = st.text_area(
            "Agenda items, one per line",
            value="\n".join(DEFAULT_AGENDA_ITEMS),
            height=150,
        )
        members_present_text = st.text_area(
            "Names of members present, one per line",
            value="\n".join(DEFAULT_MEMBERS),
            height=150,
        )
        resolution_text = st.text_area(
            "Resolution text (optional; leave blank for a professional default)",
            value="",
            height=140,
        )

        submitted = st.form_submit_button("Generate document")

    if not submitted:
        return

    try:
        generated_path = generate_document(
            document_type=document_type,
            meeting_type=meeting_type,
            meeting_date=meeting_date,
            meeting_time=meeting_time,
            venue=venue,
            agenda_items=_split_lines(agenda_items_text),
            members_present=_split_lines(members_present_text),
            chairperson_name=chairperson_name,
            secretary_name=secretary_name,
            resolution_subject=resolution_subject,
            resolution_text=resolution_text,
        )

        log_id = add_document_log(
            document_type=document_type,
            meeting_date=meeting_date.isoformat(),
            file_path=str(generated_path),
        )

        email_status = "Not sent"
        if send_email:
            subject = f"{EMAIL_SUBJECT_PREFIX} - {document_type}"
            body = (
                "Dear Sir/Madam,\n\n"
                "Please find attached the generated compliance document for review, "
                "signature, and physical filing.\n\n"
                f"Regards,\n{SOCIETY_DETAILS['name']}"
            )
            success, message = send_email_with_attachments(
                sender_email=sender_email,
                recipient_email=recipient_email,
                subject=subject,
                body=body,
                attachment_paths=[generated_path],
            )
            email_status = "Sent" if success else f"Failed: {message}"
            update_email_status(log_id, email_status)

            if success:
                st.success(message)
            else:
                st.warning(message)
        else:
            update_email_status(log_id, email_status)

        st.success(f"Document generated: {generated_path}")
        st.download_button(
            label="Download DOCX",
            data=_read_file_bytes(generated_path),
            file_name=generated_path.name,
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        )

    except Exception as exc:  # Streamlit should display friendly errors instead of a crash page.
        st.error(f"Could not generate document: {exc}")


def compliance_reminder_module() -> None:
    st.subheader("Compliance Reminders")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        last_gb_meeting = st.date_input("Last GB meeting", value=date.today())
    with col2:
        last_agm = st.date_input("Last AGM", value=date.today())
    with col3:
        last_audit = st.date_input("Last audit", value=date.today())
    with col4:
        last_election = st.date_input("Last election", value=date.today())

    reminders = build_compliance_reminders(
        last_gb_meeting=last_gb_meeting,
        last_agm=last_agm,
        last_audit=last_audit,
        last_election=last_election,
    )
    reminder_rows = [
        {
            "Compliance Item": item.compliance_item,
            "Frequency": item.frequency,
            "Last Completed": item.last_completed,
            "Next Due": item.next_due,
            "Status": item.status,
            "Note": item.note,
        }
        for item in reminders
    ]
    st.dataframe(pd.DataFrame(reminder_rows), use_container_width=True)


def compliance_rules_module() -> None:
    st.subheader("Compliance Rules Reference")
    st.table(pd.DataFrame(COMPLIANCE_RULES.items(), columns=["Rule", "Requirement"]))


def document_log_module() -> None:
    st.subheader("Generated Document Log")
    rows = fetch_document_logs()
    if not rows:
        st.info("No documents generated yet.")
        return

    df = pd.DataFrame(
        rows,
        columns=[
            "ID",
            "Document Type",
            "Date Generated",
            "Meeting Date",
            "File Path",
            "Email Status",
        ],
    )
    st.dataframe(df, use_container_width=True)


def sidebar_help() -> None:
    st.sidebar.header("Email setup")
    st.sidebar.write("Email defaults are loaded from `.env`.")
    st.sidebar.code(f"{GMAIL_PASSWORD_ENV_VAR}=your_gmail_app_password", language="text")
    st.sidebar.write("Use a Gmail app password, not your normal Gmail password.")


def main() -> None:
    init_db()
    show_header()
    sidebar_help()

    tab_document, tab_reminders, tab_log, tab_rules = st.tabs(
        ["Documents", "Reminders", "Log", "Rules"]
    )
    with tab_document:
        document_form()
    with tab_reminders:
        compliance_reminder_module()
    with tab_log:
        document_log_module()
    with tab_rules:
        compliance_rules_module()


if __name__ == "__main__":
    main()
