"""Compliance reminder calculations for society governance."""

from dataclasses import dataclass
from datetime import date, timedelta
from typing import List, Optional


@dataclass
class ComplianceReminder:
    compliance_item: str
    frequency: str
    last_completed: Optional[date]
    next_due: Optional[date]
    status: str
    note: str


def _status_for_due_date(next_due: Optional[date], today: date) -> str:
    if next_due is None:
        return "Date needed"
    if next_due < today:
        return "Overdue"
    if next_due <= today + timedelta(days=30):
        return "Due soon"
    return "Upcoming"


def build_compliance_reminders(
    last_gb_meeting: Optional[date],
    last_agm: Optional[date],
    last_audit: Optional[date],
    last_election: Optional[date],
    today: Optional[date] = None,
) -> List[ComplianceReminder]:
    """Return reminders for key society compliance events."""
    today = today or date.today()

    items = [
        (
            "Governing Body Meeting",
            "Every 3 months",
            last_gb_meeting,
            last_gb_meeting + timedelta(days=90) if last_gb_meeting else None,
            "Minimum frequency under the provided compliance rules.",
        ),
        (
            "Annual General Meeting",
            "Once every year",
            last_agm,
            last_agm + timedelta(days=365) if last_agm else None,
            "AGM should be held annually and minutes should be filed physically.",
        ),
        (
            "Audit",
            "Once every year",
            last_audit,
            last_audit + timedelta(days=365) if last_audit else None,
            "Annual accounts must be audited.",
        ),
        (
            "Election",
            "Every 5 years",
            last_election,
            last_election + timedelta(days=365 * 5) if last_election else None,
            "Governing Body election cycle as provided.",
        ),
    ]

    return [
        ComplianceReminder(
            compliance_item=name,
            frequency=frequency,
            last_completed=last_done,
            next_due=next_due,
            status=_status_for_due_date(next_due, today),
            note=note,
        )
        for name, frequency, last_done, next_due, note in items
    ]
