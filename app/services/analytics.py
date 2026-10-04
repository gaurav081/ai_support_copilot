from collections import Counter

from app.database.database import SessionLocal
from app.database.models import AnalyticsEvent


def record_analytics(
    conversation_id: str,
    prompt: str,
    intent: str,
    sentiment: str,
    priority: str,
    response_time: float,
    escalated: bool
) -> None:

    db = SessionLocal()

    try:

        event = AnalyticsEvent(
            conversation_id=conversation_id,
            prompt=prompt,
            intent=intent,
            sentiment=sentiment,
            priority=priority,
            response_time=response_time,
            escalated=escalated
        )

        db.add(event)
        db.commit()

    finally:

        db.close()


def get_analytics() -> list[dict]:

    db = SessionLocal()

    try:

        events = (
            db.query(AnalyticsEvent)
            .order_by(AnalyticsEvent.created_at.desc())
            .all()
        )

        return [
            {
                "id": event.id,
                "conversation_id": event.conversation_id,
                "prompt": event.prompt,
                "intent": event.intent,
                "sentiment": event.sentiment,
                "priority": event.priority,
                "response_time": event.response_time,
                "escalated": event.escalated,
                "created_at": event.created_at.isoformat()
            }
            for event in events
        ]

    finally:

        db.close()


def get_metrics() -> dict:

    db = SessionLocal()

    try:

        events = db.query(AnalyticsEvent).all()

        total_requests = len(events)

        if total_requests == 0:
            return {
                "total_requests": 0,
                "average_response_time": 0,
                "escalated_requests": 0,
                "escalation_rate": 0,
                "intent_distribution": {},
                "priority_distribution": {}
            }

        average_response_time = (
            sum(
                event.response_time
                for event in events
            )
            / total_requests
        )

        escalated_requests = sum(
            event.escalated
            for event in events
        )

        intent_distribution = Counter(
            event.intent
            for event in events
        )

        priority_distribution = Counter(
            event.priority
            for event in events
        )

        return {
            "total_requests": total_requests,
            "average_response_time": round(
                average_response_time,
                2
            ),
            "escalated_requests": escalated_requests,
            "escalation_rate": round(
                escalated_requests / total_requests,
                3
            ),
            "intent_distribution": dict(
                intent_distribution
            ),
            "priority_distribution": dict(
                priority_distribution
            )
        }

    finally:

        db.close()
