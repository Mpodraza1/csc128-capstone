import logging

import streamlit as st

from conversation import new_state, respond

st.title("Alternate Tuning Assistant")
st.caption(
    "This is an AI software assistant for exploring guitar tunings."
)
st.write(
    "Commands: **analyze**, **transpose**, **create**, **ideas**, **reset**."
)

if "messages" not in st.session_state:
    st.session_state.messages = []
if "bot_state" not in st.session_state:
    st.session_state.bot_state = new_state()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if prompt := st.chat_input("Enter your message"):
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )
    with st.chat_message("user"):
        st.write(prompt)

    # Unexpected failures stay out of the user-facing chat.
    try:
        try:
            api_key = st.secrets.get("GROQ_API_KEY", "")
        except Exception:
            api_key = ""

        with st.spinner("Working…"):
            reply = respond(
                prompt, st.session_state.bot_state, api_key
            )
    except Exception:
        logging.exception("Chat request failed")
        reply = (
            "Something went wrong. Please try again, "
            "or type reset to start a new request."
        )

    st.session_state.messages.append(
        {"role": "assistant", "content": reply}
    )
    with st.chat_message("assistant"):
        st.write(reply)
