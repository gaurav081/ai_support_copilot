import requests
import streamlit as st


API_URL = "http://127.0.0.1:8000"


st.set_page_config(
    page_title="AI Support Copilot",
    page_icon="💬",
    layout="centered"
)


st.title("AI Support Copilot")
st.caption("Customer support assistant powered by RAG, tools, and FastAPI")


# Create a conversation ID for this browser session.
if "conversation_id" not in st.session_state:
    st.session_state.conversation_id = "streamlit-user-1"


# Store messages only for displaying them in the UI.
if "messages" not in st.session_state:
    st.session_state.messages = []


# Display previous messages.
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# Chat input.
prompt = st.chat_input("How can I help you?")


if prompt:

    # Display user's message immediately.
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    # Send request to FastAPI.
    try:
        response = requests.post(
            f"{API_URL}/chat",
            json={
                "conversation_id": st.session_state.conversation_id,
                "prompt": prompt
            },
            timeout=120
        )

        response.raise_for_status()

        data = response.json()

        answer = data["response"]

        # Display assistant response.
        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )

        with st.chat_message("assistant"):
            st.markdown(answer)

            # Show analysis information.
            with st.expander("Message analysis"):
                st.write(
                    f"**Intent:** {data['analysis']['intent']}"
                )
                st.write(
                    f"**Sentiment:** {data['analysis']['sentiment']}"
                )
                st.write(
                    f"**Priority:** {data['analysis']['priority']}"
                )

            # Show knowledge-base sources when available.
            if data["sources"]:
                with st.expander("Sources"):
                    for source in data["sources"]:
                        st.write(
                            f"**Source:** {source['source']}"
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
