import re

NOTE_VALUES = {
    "C": 0, "D": 2, "E": 4, "F": 5,
    "G": 7, "A": 9, "B": 11,
}

NOTE_NAMES = [
    "C", "C#", "D", "D#", "E", "F",
    "F#", "G", "G#", "A", "A#", "B",
]

INTERVAL_NAMES = [
    "unison", "minor second", "major second",
    "minor third", "major third", "perfect fourth",
    "tritone", "perfect fifth", "minor sixth",
    "major sixth", "minor seventh", "major seventh",
]


def parse_note(token):
    match = re.fullmatch(r"([A-Ga-g])([#b]?)([0-8])", token)
    if not match:
        raise ValueError(
            f"Invalid note: {token}. Use a note with an octave "
            "number, such as E2, F#2, or Bb2."
        )

    letter, accidental, octave = match.groups()
    adjustment = {"": 0, "#": 1, "b": -1}[accidental]
    pitch = (
        12 * (int(octave) + 1)
        + NOTE_VALUES[letter.upper()]
        + adjustment
    )

    if not 12 <= pitch <= 119:
        raise ValueError("Please use pitches within octaves 0–8.")

    return pitch


def parse_tuning(text):
    """Read the complete tuning from lowest string to highest."""
    tokens = text.replace(",", " ").split()
    if len(tokens) not in (6, 7, 8):
        raise ValueError(
            "Please enter the complete tuning as 6, 7, or 8 "
            "note names with octave numbers. For example: "
            "E2 A2 D3 G3 B3 E4."
        )

    pitches = [parse_note(token) for token in tokens]

    if any(b < a for a, b in zip(pitches, pitches[1:])):
        raise ValueError(
            "Enter strings from lowest pitch to highest pitch."
        )

    return pitches


def format_tuning(pitches):
    return " ".join(
        f"{NOTE_NAMES[pitch % 12]}{pitch // 12 - 1}"
        for pitch in pitches
    )


def analyze_tuning(pitches):
    results = []
    for index, (low, high) in enumerate(zip(pitches, pitches[1:]), 1):
        distance = high - low
        octaves, remainder = divmod(distance, 12)

        if distance == 0:
            name = "unison"
        elif remainder == 0:
            name = "octave" if octaves == 1 else f"{octaves} octaves"
        else:
            name = INTERVAL_NAMES[remainder]
            if octaves:
                name += f" plus {octaves} octave(s)"

        results.append(
            f"Strings {index}–{index + 1}: "
            f"{distance} semitones ({name})"
        )

    return "\n".join(results)


def transpose_tuning(pitches, semitones):
    # Moving every string equally preserves all intervals.
    shifted = [pitch + semitones for pitch in pitches]
    if any(pitch < 12 or pitch > 119 for pitch in shifted):
        raise ValueError(
            "The result falls outside supported octaves 0–8."
        )
    return shifted
