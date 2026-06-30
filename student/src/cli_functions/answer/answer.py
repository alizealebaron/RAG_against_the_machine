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
# @update   : 2026/06/30 15:30:07 by alebaron                                #
# ************************************************************************** #

# +-------------------------------------------------------------------------+
# |                              Importation                                |
# +-------------------------------------------------------------------------+

import os
import json
import torch
from transformers import pipeline
from ...models.models import Chunk, StudentSearchResults
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

    def answer_single(this) -> None:

        # Génération de la recherche pour une réponse unique

        searchModel = Search(this.__k, this.__question)
        search_result = searchModel.search_single()

        # Génération du prompt
        start_prompt = this.__init_prompt(search_result)

        # Génération de la réponse
        chat = [
            {"role": "system", "content": start_prompt},
            {"role": "user", "content": this.__question}
        ]

        response = this.__pipeline(chat, max_new_tokens=512)
        reponse = response[0]["generated_text"][-1]["content"]

        print(reponse)

        print("--------------------------------")

        rep = reponse.split("</think>")
        print(rep[1])

        # Renvoie de la réponse

    # +---------------------------------------------------------------------+
    # |                           Prompt Methods                            |
    # +---------------------------------------------------------------------+

    def __init_prompt(this, search_result: StudentSearchResults) -> str:

        start_prompt = ("You are a robot that must answer the questions "
                        "asked of you in a simple way, using the information"
                        " from the texts I will give you. I want really short "
                        "answer.\n\n"
                        "Here are the texts: \n")

        for chunk in search_result.search_results[0].retrieved_sources:
            start_prompt += f"- {chunk.file_path}:\n"
            start_prompt += f"{chunk.text}\n\n"

        return start_prompt

    # +---------------------------------------------------------------------+
    # |                           Others Methods                            |
    # +---------------------------------------------------------------------+

    def __is_path_init(this, path: str) -> bool:

        if (path is not None):
            return os.path.exists(path)
        return True
