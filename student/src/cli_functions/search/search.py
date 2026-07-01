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
# @update   : 2026/07/01 16:56:47 by alebaron                                #
# ************************************************************************** #

# +-------------------------------------------------------------------------+
# |                              Importation                                |
# +-------------------------------------------------------------------------+

import os
import json
import bm25s
from tqdm import tqdm
from ...utils.error import IndexError, SearchError, print_error
from ...models.models import Chunk, StudentSearchResults, MinimalSearchResults
from ...models.models import RagDataset

# +-------------------------------------------------------------------------+
# |                                 CONST                                   |
# +-------------------------------------------------------------------------+


INDEX_PATH = "../data/processed/chunks/chunk.json"
BM25_PATH = "../data/processed/bm25_index"


# +-------------------------------------------------------------------------+
# |                                 Class                                   |
# +-------------------------------------------------------------------------+

class Search():

    # +---------------------------------------------------------------------+
    # |                                 Init                                |
    # +---------------------------------------------------------------------+

    def __init__(this, k: int, question=None,
                 dataset_path=None, save_path=None):

        # Erreur si jamais l'index n'est pas initialisé
        if (this.__is_path_init(INDEX_PATH) is False):
            raise IndexError("Error: You must do indexing before searching.")

        # Récupération des données
        with open(INDEX_PATH, "r") as file:
            data = json.load(file)

        # Initialisation des attributs
        this.__lst_chunk = [Chunk(**arg) for arg in data]
        this.__retriever = bm25s.BM25.load(BM25_PATH, mmap=True)
        this.__k = k
        this.__question = question
        this.__dataset_path = dataset_path
        this.__save_path = save_path

        if (this.__dataset_path is not None):
            if (this.__is_path_init(this.__dataset_path) is False):
                raise Exception(f"Cannot found {this.__dataset_path}.")

        if (int(this.__k) < 1):
            print_error(SearchError(), f"k value can't be negativ ({k}) "
                        "default value will be used (5).")
            this.__k = 5

    # +---------------------------------------------------------------------+
    # |                           Search Methods                            |
    # +---------------------------------------------------------------------+

    def search_single(this) -> StudentSearchResults:

        search = this.__get_min_search_result("single_query", this.__question)
        search_result = StudentSearchResults(search_results=[], k=this.__k)
        search_result.search_results.append(search)

        return search_result

    def search_dataset(this) -> None:

        # Récupération du dataset et des questions
        with open(this.__dataset_path, "r") as file:
            data = json.load(file)
        dataset = RagDataset(**data)

        # Boucle sur toutes les réponses pour récupérer les données
        search_result = StudentSearchResults(search_results=[], k=this.__k)

        nb_doc = len(dataset.rag_questions)
        progress_bar = tqdm(total=nb_doc, desc="Searching data in chunk")

        try:

            for question in dataset.rag_questions:

                search = this.__get_min_search_result(question.question_id,
                                                      question.question)
                search_result.search_results.append(search)

                progress_bar.update(1)

        except Exception as e:
            raise Exception(e)

        finally:
            progress_bar.close()

        # Enregistrement des résultats
        res = search_result.model_dump_json(indent=2)

        name = os.path.basename(this.__dataset_path)
        output_file = os.path.join(this.__save_path, name)

        os.makedirs(this.__save_path, exist_ok=True)
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(res)

        print(f"Saved student_search_results to {this.__save_path}{name}")

    # +---------------------------------------------------------------------+
    # |                           Others Methods                            |
    # +---------------------------------------------------------------------+

    def __get_min_search_result(this, id: str,
                                question: str) -> MinimalSearchResults:

        min_search_res = MinimalSearchResults(question_id=id,
                                              question_str=question,
                                              retrieved_sources=[])

        query_tokens = bm25s.tokenize(question)
        docs, scores = this.__retriever.retrieve(query_tokens,
                                                 k=this.__k)

        for doc_id in docs[0]:

            idx = int(doc_id)

            if 0 <= idx < len(this.__lst_chunk):
                matching_chunk = this.__lst_chunk[idx]
                min_search_res.retrieved_sources.append(matching_chunk)

        return min_search_res

    def __is_path_init(this, path: str) -> bool:
        return os.path.exists(path)
