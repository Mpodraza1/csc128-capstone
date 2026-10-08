# Alternate Tuning Assistant

A text-based guitar-tuning chatbot for players interested in heavy,
dissonant, and atmospheric sounds. This is AI software, not a human
guitar technician.

## Public app

https://csc128-capstone-hupmbahuwfauyctcebys42.streamlit.app

## Commands

- `analyze`: Calculate intervals between adjacent strings.
- `transpose`: Move every string by a chosen number of semitones.
- `create`: Build an alternate tuning using a defined sound profile
  and provide an AI-generated explanation.
- `ideas`: Generate playing suggestions for the remembered tuning.
- `reset`: Clear the remembered tuning and pending request.

The bot asks follow-up questions for missing information and remembers
the tuning across turns within the current browser session.

## Input format

Enter the complete tuning from lowest string to highest string.
Include octave numbers. Six, seven, and eight strings are supported.

Example of C standard:

```text
C2 F2 Bb2 Eb3 G3 C4
```

Sharps and flats are accepted. Results use sharp note names.

## Example conversation

```text
User: create
Bot: What is your current tuning?
User: C2 F2 Bb2 Eb3 G3 C4
Bot: What sound do you want?
User: dark and dissonant
Bot: Created tuning: C2 G2 C3 F3 F#3 G3
     [Calculated intervals and AI explanation follow.]
User: analyze
Bot: [Analyzes the remembered created tuning.]
```

Creation uses three defined profiles: dissonant, atmospheric, and heavy.
It preserves the lowest note and string count. Use transpose first
to change the lowest note. Creation changes the intervals between
strings; transposition preserves them.

## Run locally

Use Python 3.12. Download or clone this repository, open a terminal
in its folder, and run:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
mkdir -p .streamlit
```

Create `.streamlit/secrets.toml` locally with:

```toml
GROQ_API_KEY = "your-groq-api-key"
```

Then run:

```bash
python -m streamlit run app.py
```

The secrets file is excluded by `.gitignore`. Never upload it to GitHub.

## Deployment

Deploy the public GitHub repository through Streamlit Community Cloud,
using `main` as the branch and `app.py` as the entry point.

Set `GROQ_API_KEY` separately in the deployed app's Settings → Secrets.
Dependencies are pinned in `requirements.txt`.

Before submission, open the public app in a private browsing window
and test a conversation. Reopen it the night before and morning of
the deadline to reduce the risk of a sleeping app.

## Tests

Run:

```bash
python -m unittest discover -v
```

GitHub Actions also runs the tests after each commit.

Tests cover interval calculations, transposition, conversation memory,
follow-up questions, invalid-input recovery, tuning creation, playing
ideas, refusal behavior, missing keys, simulated API connection
failures, rate limits, empty results, and retry recovery.

Model calls are mocked during automated tests. Tests do not require
an API key.

## Project files

- `app.py`: Streamlit interface and session state.
- `conversation.py`: Intent routing and follow-up questions.
- `tuning_tools.py`: Note validation and exact musical calculations.
- `creative_tools.py`: Tuning profiles and creation checks.
- `llm_client.py`: Groq requests, reference loading, and API errors.
- `tuning_reference.md`: Musical reference and setup limitations.
- `test_bot.py`: Automated tests.
- `.github/workflows/tests.yml`: Automated test workflow.

## Model and reference use

Groq's `openai/gpt-oss-20b` model supplies explanations and playing
ideas. The reference document is included in its system prompt.
Python handles exact note and interval calculations.

## Limits and human handoff

The app does not listen to audio or measure actual string tension.
It refuses changes greater than two semitones up or twelve semitones
down per string in a single operation.

These are conservative project limits, not a guarantee of safety.
String gauge, scale length, and instrument setup still matter.
Consult a guitar technician about physical setup or modifications.

When the model service fails, the bot gives a readable message.
Analysis and transposition remain available.
