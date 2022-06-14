from src.util import build_nlp
import pytest

nlp = build_nlp()

class TestSectionRules:
    def test_pmh(self):
        texts = ["previous medical history", "PAST MEDICAL HISTORY"]
        docs = list(nlp.pipe(texts))
        for doc in docs:
            assert len(doc._.sections) == 1
            assert doc._.sections[0].category == "past_medical_history"
