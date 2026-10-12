from app.services.escalation import should_escalate


def test_high_priority_request_escalates():
    assert should_escalate("high", "general_question")


def test_human_assistance_request_escalates():
    assert should_escalate(
        "medium",
        "general_question",
        "I require human assistance."
    )


def test_talk_to_agent_request_escalates():
    assert should_escalate(
        "medium",
        "general_question",
        "Please connect me to an agent."
    )


def test_ordinary_shipping_question_does_not_escalate():
    assert not should_escalate(
        "medium",
        "shipping_question",
        "How long does shipping take?"
    )


def test_low_priority_general_question_does_not_escalate():
    assert not should_escalate(
        "low",
        "general_question",
        "Where can I find your FAQ?"
    )
