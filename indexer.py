import os
import argparse
from pathlib import Path
from whoosh.index import create_in
from whoosh.fields import *
from utils import Lemmatizer, get_json


def parse_qa(qa_dict):
    questions, answers = [], []
    for qa in qa_dict:
        questions.append(qa["question"])
        answers.append(qa["answer"])
    return questions, answers


def create_index(questions, answers, index_dir):
    schema = Schema(question=TEXT(stored=True), answer=TEXT(stored=True))
    if not os.path.isdir(index_dir):
        os.mkdir(index_dir)
    ix = create_in(index_dir, schema)
    writer = ix.writer()

    lemma = Lemmatizer()
    for ques, ans in zip(questions, answers):
        lemmatized_ques = lemma.lemmatize_sentence(ques)
        writer.add_document(question=lemmatized_ques, answer=ans)
    writer.commit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="You can create index with your chat history to query.",
    )
    parser.add_argument("file", type=Path, help="Parsed JSON file.")
    parser.add_argument("-o", dest="out", type=Path, help="Path for output index.")
    args = parser.parse_args()

    out_idx = args.out or "index"

    qa = get_json(args.file)
    questions, answers = parse_qa(qa)
    create_index(questions, answers, out_idx)
