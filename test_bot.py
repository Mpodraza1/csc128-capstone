import unittest
from unittest.mock import patch

import groq
import httpx

from conversation import new_state, respond
from llm_client import ask_model, ModelError
from tuning_tools import parse_tuning, analyze_tuning, format_tuning


STANDARD = "E2 A2 D3 G3 B3 E4"


class BotTests(unittest.TestCase):
    def setUp(self):
        self.state = new_state()

    def load_tuning(self, intent="analyze"):
        respond(intent, self.state)
        return respond(STANDARD, self.state)

    def test_slot_filling(self):
        answer = respond("analyze", self.state)
        self.assertIn("current tuning", answer)
        self.assertEqual(self.state["pending"], "tuning")

    def test_standard_intervals(self):
        answer = self.load_tuning()
        self.assertEqual(answer.count("5 semitones"), 4)
        self.assertEqual(answer.count("4 semitones"), 1)

    def test_memory(self):
        first = self.load_tuning()
        self.assertEqual(respond("analyze", self.state), first)

    def test_invalid_note_then_recovery(self):
        respond("analyze", self.state)
        answer = respond("E2 A2 H3 G3 B3 E4", self.state)
        self.assertIn("Invalid note", answer)
        self.assertEqual(self.state["pending"], "tuning")
        self.assertIn("5 semitones", respond(STANDARD, self.state))

    def test_transpose(self):
        self.load_tuning("transpose")
        respond("-2", self.state)
        self.assertEqual(
            format_tuning(self.state["tuning"]),
            "D2 G2 C3 F3 A3 D4",
        )

    def test_invalid_shift_then_recovery(self):
        self.load_tuning("transpose")
        self.assertIn("whole number", respond("banana", self.state))
        self.assertEqual(self.state["pending"], "shift")
        self.assertIn("Transposed tuning", respond("-2", self.state))

    def test_refusal_preserves_tuning(self):
        self.load_tuning("transpose")
        before = self.state["tuning"].copy()
        self.assertIn("cannot recommend", respond("12", self.state))
        self.assertEqual(self.state["tuning"], before)

    @patch("creative_tools.ask_model", return_value="Creative explanation.")
    def test_create(self, mocked_model):
        self.load_tuning("create")
        answer = respond("dark", self.state, "fake-key")
        self.assertIn("Created tuning", answer)
        self.assertEqual(
            format_tuning(self.state["tuning"]),
            "E2 B2 E3 A3 A#3 B3",
        )
        mocked_model.assert_called_once()

    @patch("conversation.ask_model", return_value="Three playing ideas.")
    def test_ideas(self, mocked_model):
        self.load_tuning("ideas")
        answer = respond("metal", self.state, "fake-key")
        self.assertEqual(answer, "Three playing ideas.")
        mocked_model.assert_called_once()

    def test_missing_key(self):
        with self.assertRaisesRegex(ModelError, "key is missing"):
            ask_model("Give playing ideas.", "")

    @patch("llm_client.groq.Groq")
    def test_api_connection_failure(self, mocked_client):
        request = httpx.Request("POST", "https://example.test")
        mocked_client.return_value.chat.completions.create.side_effect = (
            groq.APIConnectionError(request=request)
        )
        with self.assertRaisesRegex(ModelError, "could not be reached"):
            ask_model("Give playing ideas.", "fake-key")

    @patch("llm_client.groq.Groq")
    def test_api_rate_limit(self, mocked_client):
        request = httpx.Request("POST", "https://example.test")
        response = httpx.Response(429, request=request)
        mocked_client.return_value.chat.completions.create.side_effect = (
            groq.RateLimitError(
                "Simulated limit", response=response, body=None
            )
        )
        with self.assertRaisesRegex(ModelError, "too many requests"):
            ask_model("Give playing ideas.", "fake-key")

    @patch("llm_client.groq.Groq")
    def test_empty_model_answer(self, mocked_client):
        result = mocked_client.return_value.chat.completions.create.return_value
        result.choices = []
        with self.assertRaisesRegex(ModelError, "no answer"):
            ask_model("Give playing ideas.", "fake-key")

    @patch("conversation.ask_model")
    def test_model_failure_then_retry(self, mocked_model):
        self.load_tuning("ideas")
        mocked_model.side_effect = ModelError("Service unavailable.")
        answer = respond("metal", self.state, "fake-key")
        self.assertIn("retry", answer)
        self.assertEqual(self.state["pending"], "style")

        mocked_model.side_effect = None
        mocked_model.return_value = "Recovered answer."
        self.assertEqual(
            respond("retry", self.state, "fake-key"),
            "Recovered answer.",
        )


if __name__ == "__main__":
    unittest.main()
