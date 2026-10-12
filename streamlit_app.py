
import os
import uuid

import requests
import streamlit as st


# --------------------------------------------------
# Configuration
# --------------------------------------------------

API_URL = os.getenv(
    "BACKEND_URL",
    "http://127.0.0.1:8000"
).rstrip("/")


# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="AI Support Copilot",
    page_icon="💬",
    layout="centered"
)

st.title("AI Support Copilot")


# --------------------------------------------------
# Sidebar Navigation
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

    # Initialize conversation state.
    if "conversation_id" not in st.session_state:
        st.session_state.conversation_id = str(uuid.uuid4())

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Start a new conversation.
    if st.button(
        "New Conversation",
        use_container_width=True
    ):
        st.session_state.conversation_id = str(uuid.uuid4())
        st.session_state.messages = []
        st.rerun()

    # Display conversation history.
    for message in st.session_state.messages:

        with st.chat_message(message["role"]):
            st.markdown(message["content"])

            if message["role"] == "assistant":

                analysis = message.get("analysis", {})

                if analysis:
                    with st.expander("Copilot Details"):
                        st.write(
                            f"**Intent:** {analysis.get('intent', 'N/A')}"
                        )
                        st.write(
                            f"**Sentiment:** {analysis.get('sentiment', 'N/A')}"
                        )
                        st.write(
                            f"**Priority:** {analysis.get('priority', 'N/A')}"
                        )

                sources = message.get("sources", [])

                if sources:
                    with st.expander("Sources"):
                        for source in sources:
                            st.write(
                                f"**Source:** "
                                f"{source.get('source', 'Knowledge base')}"
                            )
                            st.write(source.get("text", ""))

    # Chat input.
    prompt = st.chat_input("How can I help you?")

    if prompt:

        # Display and store the user message.
        st.session_state.messages.append(
            {
                "role": "user",
                "content": prompt
            }
        )

        with st.chat_message("user"):
            st.markdown(prompt)

        # Send the request to FastAPI.
        with st.chat_message("assistant"):

            try:
                with st.spinner("Finding an answer..."):

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

                answer = data.get(
                    "response",
                    "The backend did not return an answer."
                )

                analysis = data.get("analysis", {})
                sources = data.get("sources", [])

                st.markdown(answer)

                if analysis:
                    with st.expander("Copilot Details"):
                        st.write(
                            f"**Intent:** {analysis.get('intent', 'N/A')}"
                        )
                        st.write(
                            f"**Sentiment:** {analysis.get('sentiment', 'N/A')}"
                        )
                        st.write(
                            f"**Priority:** {analysis.get('priority', 'N/A')}"
                        )

                if sources:
                    with st.expander("Sources"):
                        for source in sources:
                            st.write(
                                f"**Source:** "
                                f"{source.get('source', 'Knowledge base')}"
                            )
                            st.write(source.get("text", ""))

                # Store the complete assistant response.
                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer,
                        "analysis": analysis,
                        "sources": sources
                    }
                )

            except requests.exceptions.HTTPError as error:
                status_code = (
                    error.response.status_code
                    if error.response is not None
                    else "unknown"
                )

                st.error(
                    f"The support API returned HTTP {status_code}."
                )

                if error.response is not None:
                    st.caption(error.response.text[:1000])

            except requests.exceptions.Timeout:
                st.error(
                    "The request timed out. Please try again."
                )

            except requests.exceptions.RequestException as error:
                st.error(
                    "Could not connect to the AI Support API."
                )
                st.caption(str(error))

            except ValueError:
                st.error(
                    "The API returned an invalid JSON response."
                )


# --------------------------------------------------
# Admin Analytics
# --------------------------------------------------

else:

    st.header("Admin Analytics")

    st.caption(
        "Overview of customer support activity"
    )

    if st.button("Refresh Analytics"):
        st.rerun()

    try:
        response = requests.get(
            f"{API_URL}/analytics/metrics",
            timeout=15
        )

        response.raise_for_status()
        metrics = response.json()

        # Main metrics.
        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Total Requests",
                metrics.get("total_requests", 0)
            )

        with col2:
            st.metric(
                "Average Response Time",
                f"{metrics.get('average_response_time', 0)} s"
            )

        col3, col4 = st.columns(2)

        with col3:
            st.metric(
                "Escalated Requests",
                metrics.get("escalated_requests", 0)
            )

        with col4:
            escalation_rate = metrics.get(
                "escalation_rate",
                0
            )

            st.metric(
                "Escalation Rate",
                f"{escalation_rate * 100:.1f}%"
            )

        st.divider()

        # Intent distribution.
        st.subheader("Intent Distribution")

        intent_distribution = metrics.get(
            "intent_distribution",
            {}
        )

        if intent_distribution:
            st.bar_chart(intent_distribution)
        else:
            st.info("No intent data available yet.")

        # Priority distribution.
        st.subheader("Priority Distribution")

        priority_distribution = metrics.get(
            "priority_distribution",
            {}
        )

        if priority_distribution:
            st.bar_chart(priority_distribution)
        else:
            st.info("No priority data available yet.")

    except requests.exceptions.HTTPError as error:
        status_code = (
            error.response.status_code
            if error.response is not None
            else "unknown"
        )

        st.error(
            f"The analytics API returned HTTP {status_code}."
        )

        if error.response is not None:
            st.caption(error.response.text[:1000])

    except requests.exceptions.Timeout:
        st.error("The analytics request timed out.")

    except requests.exceptions.RequestException as error:
        st.error(
            "Could not connect to the AI Support API."
        )
        st.caption(str(error))

    except ValueError:
        st.error(
            "The analytics API returned invalid JSON."
        )
