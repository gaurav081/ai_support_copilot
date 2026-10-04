import uuid

import requests
import streamlit as st


API_URL = "http://127.0.0.1:8000"


st.set_page_config(
    page_title="AI Support Copilot",
    page_icon="💬",
    layout="centered"
)


st.title("AI Support Copilot")


# --------------------------------------------------
# Sidebar
# --------------------------------------------------

with st.sidebar:

    st.subheader("Navigation")

    page = st.radio(
        "Go to",
        [
            "Customer Support",
            "Admin Analytics"
        ]
    )


# --------------------------------------------------
# Customer Support
# --------------------------------------------------

if page == "Customer Support":

    st.caption(
        "Customer support assistant powered by RAG, tools, and FastAPI"
    )

    # Create a new conversation.
    if "conversation_id" not in st.session_state:
        st.session_state.conversation_id = str(
            uuid.uuid4()
        )

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if st.button(
        "New Conversation",
        use_container_width=True
    ):

        st.session_state.conversation_id = str(
            uuid.uuid4()
        )

        st.session_state.messages = []

        st.rerun()

    # Display previous messages.
    for message in st.session_state.messages:

        with st.chat_message(message["role"]):

            st.markdown(
                message["content"]
            )

            if message["role"] == "assistant":

                analysis = message.get(
                    "analysis"
                )

                if analysis:

                    with st.expander(
                        "Copilot Details"
                    ):

                        st.write(
                            f"**Intent:** "
                            f"{analysis['intent']}"
                        )

                        st.write(
                            f"**Sentiment:** "
                            f"{analysis['sentiment']}"
                        )

                        st.write(
                            f"**Priority:** "
                            f"{analysis['priority']}"
                        )

                sources = message.get(
                    "sources",
                    []
                )

                if sources:

                    with st.expander(
                        "Sources"
                    ):

                        for source in sources:

                            st.write(
                                f"**Source:** "
                                f"{source['source']}"
                            )

                            st.write(
                                source["text"]
                            )

    # Chat input.
    prompt = st.chat_input(
        "How can I help you?"
    )

    if prompt:

        st.session_state.messages.append(
            {
                "role": "user",
                "content": prompt
            }
        )

        with st.chat_message("user"):

            st.markdown(prompt)

        try:

            response = requests.post(
                f"{API_URL}/chat",
                json={
                    "conversation_id": (
                        st.session_state.conversation_id
                    ),
                    "prompt": prompt
                },
                timeout=120
            )

            response.raise_for_status()

            data = response.json()

            answer = data["response"]

            assistant_message = {
                "role": "assistant",
                "content": answer,
                "analysis": data["analysis"],
                "sources": data["sources"]
            }

            st.session_state.messages.append(
                assistant_message
            )

            with st.chat_message(
                "assistant"
            ):

                st.markdown(answer)

                with st.expander(
                    "Copilot Details"
                ):

                    st.write(
                        f"**Intent:** "
                        f"{data['analysis']['intent']}"
                    )

                    st.write(
                        f"**Sentiment:** "
                        f"{data['analysis']['sentiment']}"
                    )

                    st.write(
                        f"**Priority:** "
                        f"{data['analysis']['priority']}"
                    )

                if data["sources"]:

                    with st.expander(
                        "Sources"
                    ):

                        for source in data["sources"]:

                            st.write(
                                f"**Source:** "
                                f"{source['source']}"
                            )

                            st.write(
                                source["text"]
                            )

        except requests.exceptions.RequestException as error:

            st.error(
                "Could not connect to the AI Support API."
            )

            st.caption(
                f"Error: {error}"
            )


# --------------------------------------------------
# Admin Analytics
# --------------------------------------------------

else:

    st.header("Admin Analytics")

    st.caption(
        "Overview of customer support activity"
    )

    try:

        response = requests.get(
            f"{API_URL}/analytics/metrics",
            timeout=10
        )

        response.raise_for_status()

        metrics = response.json()

        # Main metrics
        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "Total Requests",
                metrics["total_requests"]
            )

        with col2:

            st.metric(
                "Average Response Time",
                f"{metrics['average_response_time']} s"
            )

        col3, col4 = st.columns(2)

        with col3:

            st.metric(
                "Escalated Requests",
                metrics["escalated_requests"]
            )

        with col4:

            st.metric(
                "Escalation Rate",
                f"{metrics['escalation_rate'] * 100:.1f}%"
            )

        st.divider()

        # Intent distribution
        st.subheader("Intent Distribution")

        intent_distribution = metrics[
            "intent_distribution"
        ]

        if intent_distribution:

            st.bar_chart(
                intent_distribution
            )

        else:

            st.info(
                "No intent data available yet."
            )

        # Priority distribution
        st.subheader("Priority Distribution")

        priority_distribution = metrics[
            "priority_distribution"
        ]

        if priority_distribution:

            st.bar_chart(
                priority_distribution
            )

        else:

            st.info(
                "No priority data available yet."
            )

    except requests.exceptions.RequestException as error:

        st.error(
            "Could not connect to the AI Support API."
        )

        st.caption(
            f"Error: {error}"
        )
