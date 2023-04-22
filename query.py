import argparse
import whoosh.index as index
from whoosh.qparser import QueryParser, OrGroup
from utils import Lemmatizer


def search(index_dir, query_str):
    ix = index.open_dir(index_dir)

    lemma = Lemmatizer()
    qp = QueryParser("question", schema=ix.schema, group=OrGroup)
    q = qp.parse(lemma.lemmatize_sentence(query_str))

    with ix.searcher() as searcher:
        results = searcher.search(q)
        if len(results) > 0:
            print(f"Total hits: {len(results)}")
            for hit in results:
                print(f"Answer: {hit['answer']}")
        else:
            print("No hits!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Query over index you have created.",
    )
    parser.add_argument("index", type=str, help="Index name.")
    parser.add_argument("query", type=str, help="Query (or question) string.")
    args = parser.parse_args()
    search(args.index, args.query)
