from tuning_tools import (
    parse_tuning,
    format_tuning,
    analyze_tuning,
    transpose_tuning,
)


def new_state():
    return {"tuning": None, "intent": None, "pending": None}


def tuning_question():
    return (
        "What is your tuning, from lowest string to highest? "
        "Include octaves, such as E2 A2 D3 G3 B3 E4."
    )


def continue_intent(state):
    if state["intent"] == "analyze":
        state["pending"] = None
        return analyze_tuning(state["tuning"])

    state["pending"] = "shift"
    return (
        "How many semitones should I move every string? "
        "Enter an integer: -2 means down a whole step, "
        "and 1 means up a half step."
    )


def respond(message, state):
    text = message.strip()
    command = text.lower()

    if command == "reset":
        state.update(new_state())
        return "Tuning cleared. Type analyze or transpose."

    if command in ("analyze", "transpose"):
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

    if state["pending"] == "shift":
        try:
            shift = int(text)
        except ValueError:
            return "Please enter a whole number, such as -2 or 1."

        # A conservative boundary avoids recommending large upward changes.
        # This limit is a project policy, not a guarantee of string safety.
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

    return "Type analyze, transpose, or reset."
