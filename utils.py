import json
import spacy


class Lemmatizer:
    def __init__(self, model="en_core_web_md") -> None:
        self.nlp = spacy.load(model)

    def lemmatize_sentence(self, sent):
        doc = self.nlp(sent)
        all_lemmas = [
            token.lemma_.lower() if token.lemma_ else token.text.lower()
            for token in doc
        ]
        all_lemmas = " ".join(all_lemmas).strip()
        return all_lemmas


def get_json(path):
    return json.load(path.open("r", encoding="utf8"))


def save_json(path, content):
    json.dump(content, path.open("w", encoding="utf8"), ensure_ascii=False, indent=2)
