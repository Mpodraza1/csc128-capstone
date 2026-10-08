import streamlit as st

st.title("Alternate Tuning Assistant")
st.caption(
    "This is an AI software assistant for exploring guitar tunings."
)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if prompt := st.chat_input("Ask about a guitar tuning"):
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )
    with st.chat_message("user"):
        st.write(prompt)

    reply = "The chat interface is working. Tuning features are coming next."
    st.session_state.messages.append(
        {"role": "assistant", "content": reply}
    )
    with st.chat_message("assistant"):
        st.write(reply)
