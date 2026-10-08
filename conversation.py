from tuning_tools import (
    parse_tuning,
    format_tuning,
    analyze_tuning,
    transpose_tuning,
)
from llm_client import ask_model, ModelError
from creative_tools import create_tuning


def new_state():
    return {
        "tuning": None,
        "intent": None,
        "pending": None,
        "style": None,
    }


def tuning_question():
    return (
        "What is your current tuning, from lowest string to highest? "
        "Include octaves, such as E2 A2 D3 G3 B3 E4."
    )


def continue_intent(state):
    if state["intent"] == "analyze":
        state["pending"] = None
        return analyze_tuning(state["tuning"])

    if state["intent"] in ("ideas", "create"):
        state["pending"] = "style"
        return (
            "What sound do you want? Include dark, dissonant, "
            "atmospheric, ambient, heavy, or metal."
        )

    state["pending"] = "shift"
    return (
        "How many semitones should I move every string? "
        "Enter an integer: -2 means down a whole step, "
        "and 1 means up a half step."
    )


def respond(message, state, api_key=""):
    text = message.strip()
    command = text.lower()

    if command == "reset":
        state.update(new_state())
        return "Tuning cleared. Type analyze, transpose, create, or ideas."

    if command in ("analyze", "transpose", "create", "ideas"):
        state["intent"] = command
        if state["tuning"] is None:
            state["pending"] = "tuning"
            return tuning_question()
        return continue_intent(state)

    if state["pending"] == "tuning":
        try:
            state["tuning"] = parse_tuning(text)
        except ValueError as error:
            return str(error)
        return continue_intent(state)

    if state["pending"] == "style":
        if not text:
            return "Please describe the sound you want."

        if command != "retry" or not state.get("style"):
            state["style"] = text

        try:
            if state["intent"] == "create":
                result, explanation = create_tuning(
                    state["tuning"], state["style"], api_key
                )
                # Save the new tuning only after the request succeeds.
                state["tuning"] = result
                answer = (
                    f"Created tuning: {format_tuning(result)}\n\n"
                    f"{analyze_tuning(result)}\n\n"
                    f"{explanation}\n\n"
                    "Check string tension and setup before retuning."
                )
            else:
                answer = ask_model(
                    "Suggest three simple playing ideas for this exact "
                    "tuning: an open-string combination, a simple "
                    "fretted shape with string numbers and frets, "
                    "and a rhythmic idea. String 1 means the lowest "
                    "string. Keep the response under 250 words. "
                    "Use the supplied calculated intervals.\n\n"
                    f"Tuning: {format_tuning(state['tuning'])}\n"
                    f"Intervals:\n{analyze_tuning(state['tuning'])}\n"
                    f"Desired sound: {state['style']}",
                    api_key,
                )

        except ValueError as error:
            return str(error)
        except ModelError as error:
            return f"{error}\n\nType retry to repeat this request."

        state["pending"] = None
        return answer

    if state["pending"] == "shift":
        try:
            shift = int(text)
        except ValueError:
            return "Please enter a whole number, such as -2 or 1."

        # This conservative project limit is not a safety guarantee.
        if shift > 2 or shift < -12:
            return (
                "I cannot recommend that large a tuning change. "
                "Ask a guitar technician about string gauge and setup. "
                "Enter a smaller change, or type reset."
            )

        try:
            result = transpose_tuning(state["tuning"], shift)
        except ValueError as error:
            return str(error)

        state["tuning"] = result
        state["pending"] = None
        return (
            f"Transposed tuning: {format_tuning(result)}\n\n"
            "The intervals between strings are preserved. "
            "Check string tension and instrument setup before retuning."
        )

    return "Type analyze, transpose, create, ideas, or reset."
