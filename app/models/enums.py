from enum import Enum


class ApplicationStatus(str, Enum):
    draft = "draft"
    applied = "applied"
    interview = "interview"
    offer = "offer"
    rejected = "rejected"
    withdrawn = "withdrawn"


class EventType(str, Enum):
    applied = "applied"
    recruiter_message = "recruiter_message"
    interview_scheduled = "interview_scheduled"
    interview_completed = "interview_completed"
    follow_up_sent = "follow_up_sent"
    rejection = "rejection"
    offer_received = "offer_received"
    offer_accepted = "offer_accepted"
    withdrawn = "withdrawn"

