import streamlit as st

from tuning_tools import parse_tuning, format_tuning, analyze_tuning

st.title("Alternate Tuning Assistant")
st.caption(
    "This is an AI software assistant for exploring guitar tunings."
)
st.write("Type **analyze** to examine the intervals in a tuning.")

if "messages" not in st.session_state:
    st.session_state.messages = []
if "tuning" not in st.session_state:
    st.session_state.tuning = None
if "waiting_for_tuning" not in st.session_state:
    st.session_state.waiting_for_tuning = False

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if prompt := st.chat_input("Enter your message"):
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )
    with st.chat_message("user"):
        st.write(prompt)

    if prompt.strip().lower() == "reset":
        st.session_state.tuning = None
        st.session_state.waiting_for_tuning = False
        reply = "Tuning cleared. Type analyze to start again."

    elif prompt.strip().lower() == "analyze":
        if st.session_state.tuning is None:
            st.session_state.waiting_for_tuning = True
            reply = (
                "What is your tuning, from lowest string to highest? "
                "Include octave numbers. Example: E2 A2 D3 G3 B3 E4."
            )
        else:
            reply = analyze_tuning(st.session_state.tuning)

    elif st.session_state.waiting_for_tuning:
        try:
            tuning = parse_tuning(prompt)
            st.session_state.tuning = tuning
            st.session_state.waiting_for_tuning = False
            reply = (
                f"Tuning: {format_tuning(tuning)}\n\n"
                f"{analyze_tuning(tuning)}"
            )
        except ValueError as error:
            # Keep the question active so the user can correct their input.
            reply = str(error)

    else:
        reply = (
            "Type analyze to examine a tuning, "
            "or reset to enter a different tuning."
        )

    st.session_state.messages.append(
        {"role": "assistant", "content": reply}
    )
    with st.chat_message("assistant"):
        st.write(reply)
