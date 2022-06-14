import medspacy
import os
from pathlib import Path

from medspacy.target_matcher import TargetRule
from medspacy.context import ConTextRule
from medspacy.section_detection import SectionRule
from medspacy.preprocess import PreprocessingRule
from medspacy.io import DocConsumer

RESOURCES_FOLDER = os.path.join(Path(__file__).resolve().parents[0], "resources")

DOC_CONSUMER_ATTRS = {
    "doc": ["document_classification"],
    "ent": [
        "text",
        "literal",
        "start_char",
        "end_char",
        "label_",
        "section_category" ,
        "is_negated",
        "is_uncertain",
        "is_historical",
        "is_hypothetical",
        "is_family",
        "is_ignored",
        "snippet"
            ],
    "section": DocConsumer.get_default_attrs()["section"],
    "context": DocConsumer.get_default_attrs()["context"],
}

RULE_CLASSES = {
    "concept_tagger": TargetRule,
    "target_matcher": TargetRule,
    "context": ConTextRule,
    "sectionizer": SectionRule,
    "preprocessor": PreprocessingRule
}

def build_nlp(model=None, cfg_file=None, resources_dir=None,
              doc_consumer=False, doc_consumer_attrs=None, default_rules=True,
              medspacy_components=("tokenizer", "medspacy_target_matcher", "medspacy_context", "medspacy_sectionizer")):
    """Loads an NLP model for a specified domain."""
    if model is None:
        nlp = medspacy.load("en_core_web_sm", enable=medspacy_components)
        for pipe in ('attribute_ruler', 'ner', 'lemmatizer'):
            nlp.remove_pipe(pipe)
    elif model == "medspacy":
        nlp = medspacy.load(enable=medspacy_components)
    else:
        nlp = medspacy.load(model, enable=medspacy_components)
    nlp = add_rules_from_cfg(nlp, cfg_file, resources_dir)

    if doc_consumer:
        if doc_consumer_attrs is None:
            doc_consumer_attrs = DOC_CONSUMER_ATTRS
        consumer_config = {'dtypes': tuple(doc_consumer_attrs.keys()), 'dtype_attrs': doc_consumer_attrs}
        nlp.add_pipe("medspacy_doc_consumer", config = consumer_config)

    return nlp


def add_rules_from_cfg(nlp, cfg_file=None, resources_dir=None):
    rules = load_rules_from_cfg(cfg_file, resources_dir)
    for (name, component_rules) in rules.items():
        try:
            # NOTE: This is a bit strange, but it prevents changing lots of references in code
            # to prefix with "medspacy_" when it is only needed here.
            pipe_name = name
            if name in ['concept_tagger', 'context', 'target_matcher', 'sectionizer', 'postprocessor']:
                pipe_name = 'medspacy_' + name

            component = nlp.get_pipe(pipe_name)
        except KeyError:
            raise ValueError("Invalid component:", name)
        component.add(component_rules)
    return nlp

def load_rules_from_cfg(cfg_file=None, resources_dir=None):
    if cfg_file is None:
        cfg_file = os.path.join(RESOURCES_FOLDER, "config.json")
    cfg = load_cfg_file(cfg_file)
    if resources_dir is None:
        resources_dir = RESOURCES_FOLDER
    rules = _load_cfg_rules(cfg, resources_dir)
    return rules

def load_cfg_file(filepath):
    import json
    with open(filepath) as f:
        cfg = json.loads(f.read())
    return cfg

def _load_cfg_rules(cfg, resources_dir):
    rules = dict()
    for component, filepaths in cfg["resources"][0].items():
        if component not in RULE_CLASSES:
            raise ValueError(f"Invalid component name {component} in config. "
                             f"Please add custom logic to add these rules to your pipeline. "
                             f"Valid options are: {RULE_CLASSES.keys()}")
        rule_cls = RULE_CLASSES[component]
        rules[component] = []
        for filepath in filepaths:
            abspath = os.path.abspath(os.path.join(resources_dir, filepath))

            rules[component].extend(rule_cls.from_json(abspath))
    return rules

def add_preprocess_rules(nlp):
    pass

def load_cfg_file(filepath):
    import json
    with open(filepath) as f:
        cfg = json.loads(f.read())
    return cfg