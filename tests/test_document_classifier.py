from src.util import build_nlp
import pytest

nlp = build_nlp()

class TestDocumentClassifier:
    def test_document_classifier(self):
        texts_expected = [
            ("There is no evidence of pneumonia", "NEG"),
            ("There is pneumonia", "POS")
        ]

        for text, expected in texts_expected:
            doc = nlp(text)
            actual = doc._.document_classification
            if expected != actual:
                raise ValueError(f"Incorrect document classification. "
                                 f"Expected '{expected}' and got '{actual}' "
                                 f"in doc: {doc[:10]}")

