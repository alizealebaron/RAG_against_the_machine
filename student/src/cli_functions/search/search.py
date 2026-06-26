# ************************************************************************** #
#       _  _     ____                     ,~~.                               #
#      | || |   |___  \             ,   (  ^ )>                              #
#      | || |_    __) |             )\~~'   (       _      _      _          #
#      |__   _|  / __/             (  .__)   )    >(.)__ <(^)__ =(o)__       #
#         |_|   |_____| .fr         \_.____,*      (___/  (___/  (___/       #
#                                                                            #
# ************************************************************************** #
# @name   : search.py                                                        #
# @author : alebaron <alebaron@student.42lehavre.fr>                         #
#                                                                            #
# @creation : 2026/05/15 11:16:02 by alebaron                                #
# @update   : 2026/06/26 15:43:40 by alebaron                                #
# ************************************************************************** #

# +-------------------------------------------------------------------------+
# |                              Importation                                |
# +-------------------------------------------------------------------------+

import os
import json
import bm25s
from ...utils.error import IndexError
from ...models.models import Chunk, StudentSearchResults, MinimalSearchResults

# +-------------------------------------------------------------------------+
# |                                 CONST                                   |
# +-------------------------------------------------------------------------+


INDEX_PATH = "../data/processed/chunks/chunk.json"
BM25_PATH = "../data/processed/bm25_index"


# +-------------------------------------------------------------------------+
# |                                Methods                                  |
# +-------------------------------------------------------------------------+

def cli_search(question: str, k: int):

    # On chunk les documents si ça n'a pas déjà été fait

    if (os.path.exists(INDEX_PATH) is False):
        raise IndexError("Error: You must do indexing before searching.")

    # Et ensuite on cherche les documents pertinents

    with open(INDEX_PATH, "r") as file:
        data = json.load(file)
        lst_chunk = [Chunk(**arg) for arg in data]

    corpus_texts = [chunk.text for chunk in lst_chunk]

    corpus_tokens = bm25s.tokenize(corpus_texts)
    retriever = bm25s.BM25(corpus=corpus_texts, method="bm25+")
    retriever.index(corpus_tokens)

    search = get_min_search_result("q1", question, k, retriever, lst_chunk)
    search_result = StudentSearchResults(search_results=[], k=k)
    search_result.search_results.append(search)

    


def get_min_search_result(id: str,
                          question: str,
                          k: int,
                          retriever: bm25s.BM25,
                          lst_chunk: list[Chunk]) -> MinimalSearchResults:

    min_search_res = MinimalSearchResults(question_id=id,
                                          question=question,
                                          retrieved_sources=[])

    query_tokens = bm25s.tokenize(question)
    docs, scores = retriever.retrieve(query_tokens, k=k)

    for doc in docs[0]:

        matching_chunk = next((chunk for chunk in lst_chunk if chunk.text == doc), None)

        if matching_chunk:
            min_search_res.retrieved_sources.append(matching_chunk)

    return min_search_res
