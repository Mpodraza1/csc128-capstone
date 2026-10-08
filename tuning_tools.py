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


def parse_tuning(text):
    """Read notes from lowest string to highest string."""
    tokens = text.replace(",", " ").split()
    if len(tokens) not in (6, 7, 8):
        raise ValueError("Please enter 6, 7, or 8 notes.")

    pitches = []
    for token in tokens:
        match = re.fullmatch(r"([A-Ga-g])([#b]?)([0-8])", token)
        if not match:
            raise ValueError(
                f"Invalid note: {token}. Use notes with octaves, "
                "such as E2 or Bb2."
            )

        letter, accidental, octave = match.groups()
        adjustment = {"": 0, "#": 1, "b": -1}[accidental]
        pitch = (
            12 * (int(octave) + 1)
            + NOTE_VALUES[letter.upper()]
            + adjustment
        )
        pitches.append(pitch)

    if any(b < a for a, b in zip(pitches, pitches[1:])):
        raise ValueError("Enter strings from lowest pitch to highest pitch.")

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
        name = (
            "octave" if distance == 12
            else INTERVAL_NAMES[distance % 12]
        )
        if distance > 12:
            name += f" plus {distance // 12} octave(s)"
        results.append(
            f"Strings {index}–{index + 1}: "
            f"{distance} semitones ({name})"
        )
    return "\n".join(results)


def transpose_tuning(pitches, semitones):
    # Moving every string equally preserves all intervals.
    shifted = [pitch + semitones for pitch in pitches]
    if any(pitch < 12 or pitch > 119 for pitch in shifted):
        raise ValueError("The result falls outside supported octaves 0–8.")
    return shifted
