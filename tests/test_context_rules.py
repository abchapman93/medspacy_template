from src.util import build_nlp
from tests.util import testutils
import pytest

nlp = build_nlp()

class TestContextModifiers:
    def test_consolidation_negated(self):
        text = "no evidence of pna"
        doc = nlp(text)

        msg = testutils.test_entity_modifier_extension_true(doc, 'pna', 'is_negated')

        assert (msg == '')