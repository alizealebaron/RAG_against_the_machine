# ************************************************************************** #
#       _  _     ____                     ,~~.                               #
#      | || |   |___  \             ,   (  ^ )>                              #
#      | || |_    __) |             )\~~'   (       _      _      _          #
#      |__   _|  / __/             (  .__)   )    >(.)__ <(^)__ =(o)__       #
#         |_|   |_____| .fr         \_.____,*      (___/  (___/  (___/       #
#                                                                            #
# ************************************************************************** #
# @name   : answer.py                                                        #
# @author : alebaron <alebaron@student.42lehavre.fr>                         #
#                                                                            #
# @creation : 2026/05/15 10:54:32 by alebaron                                #
# @update   : 2026/07/01 17:04:13 by alebaron                                #
# ************************************************************************** #

# +-------------------------------------------------------------------------+
# |                              Importation                                |
# +-------------------------------------------------------------------------+

import os
import json
import torch
from transformers import pipeline
from ...models.models import Chunk, StudentSearchResults, MinimalAnswer
from ...models.models import StudentSearchResultsAndAnswer
from ...utils.error import AnswerError, print_error
from ..search.search import Search

# +-------------------------------------------------------------------------+
# |                                 CONST                                   |
# +-------------------------------------------------------------------------+


INDEX_PATH = "../data/processed/chunks/chunk.json"


# +-------------------------------------------------------------------------+
# |                                 Class                                   |
# +-------------------------------------------------------------------------+

class Answer():

    # +---------------------------------------------------------------------+
    # |                                 Init                                |
    # +---------------------------------------------------------------------+

    def __init__(this, k: int, question=None, search_path=None,
                 save_path=None):

        # Récupération des données
        with open(INDEX_PATH, "r") as file:
            data = json.load(file)

        # Initialisation des attributs
        this.__k = k
        this.__question = question
        this.__search_path = search_path
        this.__save_path = save_path
        this.__lst_chunk = [Chunk(**arg) for arg in data]

        # Vérification des prédispositions pour l'answer
        if (this.__is_path_init(this.__search_path) is False):
            raise AnswerError(f"Cannot find {search_path}. Do search before.")

        if (int(this.__k) < 1):
            print_error(AnswerError(), f"k value can't be negativ ({k})."
                        "default value will be used (5).")
            this.__k = 5

        # Initialisation du prompt inital

        this.__pipeline = pipeline(task="text-generation",
                                   model="Qwen/Qwen3-0.6B",
                                   dtype=torch.bfloat16,
                                   device=-1)

    # +---------------------------------------------------------------------+
    # |                           Answer Methods                            |
    # +---------------------------------------------------------------------+

    def answer_single(this) -> StudentSearchResultsAndAnswer:

        # Génération de la recherche pour une réponse unique

        searchModel = Search(this.__k, this.__question)
        search_result = searchModel.search_single()
        question = search_result.search_results[0]

        # Génération du prompt
        start_prompt = this.__init_prompt_sys()
        user_prompt = this.__init_prompt_usr(search_result)

        # Génération de la réponse
        chat = [
            {"role": "system", "content": start_prompt},
            {"role": "user", "content": user_prompt}
        ]

        response = this.__pipeline(chat, max_new_tokens=256)
        reponse = response[0]["generated_text"][-1]["content"]
        rep = reponse.split("</think>\n\n")

        # Renvoie de la réponse
        min_ans = MinimalAnswer(answer=rep[1],
                                question_id=question.question_id,
                                question_str=question.question_str,
                                retrieved_sources=question.retrieved_sources)

        answer = StudentSearchResultsAndAnswer(k=this.__k,
                                               search_results=[min_ans])

        return answer

    def answer_dataset(this) -> StudentSearchResultsAndAnswer:

        pass

    # +---------------------------------------------------------------------+
    # |                           Answer Methods                            |
    # +---------------------------------------------------------------------+

    def answer_one_question(this) -> MinimalAnswer:

        pass

    # +---------------------------------------------------------------------+
    # |                           Prompt Methods                            |
    # +---------------------------------------------------------------------+

    def __init_prompt_sys(this) -> str:

        start_prompt = ("You are a helpful assistant expert in LLM domain. "
                        "Answer the question using the provided context. "
                        "Be concise and precise. Answer: /no_think")

        return start_prompt

    def __init_prompt_usr(this, shrc_res: StudentSearchResults) -> str:

        contexte = []

        for chunk in shrc_res.search_results[0].retrieved_sources:

            contexte.append(f"[Source: {chunk.file_path}]\n{chunk.text}")

        contexte = "\n\n---\n\n".join(contexte)
        start_prompt = (f"Contexte: {contexte}\n\n"
                        f"Question : {this.__question}")

        return start_prompt

    # +---------------------------------------------------------------------+
    # |                           Others Methods                            |
    # +---------------------------------------------------------------------+

    def __is_path_init(this, path: str) -> bool:

        if (path is not None):
            return os.path.exists(path)
        return True
