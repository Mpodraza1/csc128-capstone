from llm_client import ask_model
from tuning_tools import format_tuning, analyze_tuning


def create_tuning(current_tuning, style, api_key):
    description = style.lower()

    if any(word in description for word in (
        "dark", "dissonant", "horror", "experimental",
    )):
        profile = "dissonant"
        offsets = [0, 7, 12, 17, 18, 19, 24, 25]

    elif any(word in description for word in (
        "atmospheric", "ambient", "open",
    )):
        profile = "atmospheric"
        offsets = [0, 7, 12, 19, 24, 26, 31, 38]

    elif any(word in description for word in (
        "heavy", "metal", "low",
    )):
        profile = "heavy"
        offsets = [0, 7, 12, 17, 21, 26, 31, 36]

    else:
        raise ValueError(
            "Please include dark, dissonant, atmospheric, "
            "ambient, heavy, or metal in your description."
        )

    # Keep the lowest note and string count; change the other intervals.
    lowest = current_tuning[0]
    result = [
        lowest + offset
        for offset in offsets[:len(current_tuning)]
    ]

    if any(pitch < 12 or pitch > 119 for pitch in result):
        raise ValueError(
            "This tuning falls outside supported octaves 0–8. "
            "Try another starting tuning."
        )

    # Apply the same conservative change limits used for transposition.
    changes = [
        new - old for old, new in zip(current_tuning, result)
    ]
    if any(change > 2 or change < -12 for change in changes):
        raise ValueError(
            "This pattern would require too large a change "
            "from your current tuning. Try another sound profile, "
            "or consult a guitar technician about the setup."
        )

    explanation = ask_model(
        "Briefly explain this proposed alternate tuning in under "
        "150 words. Connect its calculated intervals to the desired "
        "sound, and give one simple playing idea. "
        "Do not suggest different notes or guarantee physical safety.\n\n"
        f"Profile: {profile}\n"
        f"Desired sound: {style}\n"
        f"Tuning: {format_tuning(result)}\n"
        f"Calculated intervals:\n{analyze_tuning(result)}",
        api_key,
    )

    return result, explanation
