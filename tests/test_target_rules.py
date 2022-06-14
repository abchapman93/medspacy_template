from src.util import build_nlp
import pytest

nlp = build_nlp()

class TestTargetRules:
    def test_pneumonia(self):
        texts = ["pneumonia", "pna"]
        docs = list(nlp.pipe(texts))
        for doc in docs:
            assert len(doc.ents) == 1
            assert doc.ents[0].label_ == "PNEUMONIA"
