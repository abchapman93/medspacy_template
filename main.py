from src.util import build_nlp

if __name__ == "__main__":
    nlp = build_nlp(doc_consumer=True)
    print(nlp.pipe_names)
    texts = [
        "Pneumonia was confirmed with an X-Ray.",
        "Past Medical Hx: Pneumonia",
        "No evidence of pna."
    ]
    docs = list(nlp.pipe(texts))
    print("", "section_category", "is_negated", "is_historical", "is_positive_existence", sep="\t")
    for doc in docs:
        print(doc)
        for ent in doc.ents:
            print("\t",ent, ent._.section_category, ent._.is_negated, ent._.is_historical, ent._.is_positive_existence)

        print(doc._.to_dataframe("ent"))
