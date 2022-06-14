from spacy import Language

@Language.factory("custom_document_classifier")
class DocumentClassifier:
    """
    """
    name = "document_classifier"

    _TARGET_CLASSES = set()

    def __init__(self, nlp, name="document_classifier", debug=False):
        self.debug = debug
        pass

    def __call__(self, doc, **kwargs):
        doc._.document_classification = self.classify_document(doc, **kwargs)
        return doc

    def classify_document(self, doc, **kwargs):
        classification = self._classify_document(doc, **kwargs)
        return classification

    def _classify_document(self, doc, **kwargs):
        for ent in doc.ents:
            if ent.label_ == "PNEUMONIA" and ent._.is_asserted:
                if self.debug:
                    print("Found asserted entity:", ent)
                return "POS"
        if self.debug:
            print(f"No asserted ents: {doc.ents}")
        return "NEG"

