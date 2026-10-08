import streamlit as st

from conversation import new_state, respond

st.title("Alternate Tuning Assistant")
st.caption(
    "This is an AI software assistant for exploring guitar tunings."
)
st.write(
    "Type **analyze** to examine intervals, "
    "**transpose** to shift a tuning, "
    "or **reset** to start again."
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

    reply = respond(prompt, st.session_state.bot_state)

    st.session_state.messages.append(
        {"role": "assistant", "content": reply}
    )
    with st.chat_message("assistant"):
        st.write(reply)
