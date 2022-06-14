from spacy.tokens import Token, Span, Doc

def set_extensions(ignore_errors=True):
    "Set custom medspaCy extensions for Token, Span, and Doc classes."
    set_token_extensions(ignore_errors)
    set_span_extensions(ignore_errors)
    set_doc_extensions(ignore_errors)

def set_token_extensions(ignore_errors=True):
    for attr, attr_info in _token_extensions.items():
        try:
            Token.set_extension(attr, force=True, **attr_info)
        except Exception as e: # If the attribute has already set, this will raise an error
            if not ignore_errors:
                raise e

def set_span_extensions(ignore_errors=True):
    for attr, attr_info in _span_extensions.items():
        try:
            Span.set_extension(attr, force=True, **attr_info)
        except Exception as e: # If the attribute has already set, this will raise an error
            if not ignore_errors:
                raise e

def set_doc_extensions(ignore_errors=True):
    for attr, attr_info in _doc_extensions.items():
        try:
            Doc.set_extension(attr, force=True, **attr_info)
        except Exception as e: # If the attribute has already set, this will raise an error
            if not ignore_errors:
                raise e

def get_positive_existence(span):
    """Naive getter function where of the span is modified, take the first one."""
    for modifier in span._.modifiers:
        if modifier.category == "POSITIVE_EXISTENCE":
            return True
    return True


def get_snippet(span, window=10, max_len=200):
    snippet = span._.window(window, left=True, right=True).text
    if len(snippet) > max_len:
        snippet = snippet[:max_len]
    return snippet

def get_literal(span):
    rule = span._.target_rule
    if rule is None:
        return span.text.lower()
    return rule.literal

_span_extensions = {
    "is_positive_existence": {"getter": get_positive_existence},
    # some of these below we may not use in our present 2021 Pneumonia project, but since they are in Moonstone and could be helpful,
    # I have added these here
    "is_ignored": {"default": False},
    "snippet": {"getter": get_snippet},
    "literal": {"getter": get_literal}
}

_doc_extensions = {
    "document_classification": {"default": None},
}

_token_extensions = {

}