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
# @update   : 2026/07/02 15:08:49 by alebaron                                #
# ************************************************************************** #

# +-------------------------------------------------------------------------+
# |                              Importation                                |
# +-------------------------------------------------------------------------+

import os
import json
import torch
from tqdm import tqdm
from transformers import pipeline
from ...models.models import StudentSearchResults, MinimalAnswer
from ...models.models import StudentSearchResultsAndAnswer
from ...models.models import MinimalSearchResults
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

    def __init__(this, k: int, question: str | None = None,
                 search_path: str | None = None,
                 save_path: str | None = None) -> None:

        # Initialisation des attributs
        this.__k = k
        this.__question = question
        this.__search_path = search_path
        this.__save_path = save_path

        # Vérification des prédispositions pour l'answer
        if (this.__is_path_init(this.__search_path) is False):
            raise AnswerError(f"Cannot find {search_path}. Do search before.")

        if (int(this.__k) < 1):
            print_error(AnswerError(), f"k value can't be < 1({k})."
                                       "default value will be used (5).")
            this.__k = 5

        # Initialisation du prompt inital
        this.__pipeline = pipeline(task="text-generation",
                                   model="Qwen/Qwen3-0.6B",
                                   dtype=torch.bfloat16,
                                   device_map="auto")

    # +---------------------------------------------------------------------+
    # |                           Answer Methods                            |
    # +---------------------------------------------------------------------+

    def answer_single(this) -> StudentSearchResultsAndAnswer:

        # Génération de la recherche pour une réponse unique

        searchModel = Search(this.__k, this.__question)
        search_result = searchModel.search_single()
        question = search_result.search_results[0]

        # Réponse à la question
        min_ans = this.__answer_one_question(question)

        # Mise sous la bonne forme de rendu
        answer = StudentSearchResultsAndAnswer(k=this.__k,
                                               search_results=[min_ans])

        return answer

    def answer_dataset(this) -> None:

        if this.__search_path is None:
            raise AnswerError("Search results path is missing.")

        if this.__save_path is None:
            raise AnswerError("Save path is missing.")

        # Récupération des résultats du search pour les datasets
        with open(this.__search_path, "r") as file:
            data = json.load(file)

        dataset = StudentSearchResults(**data)

        # Initialisation du format de réponse
        answer = StudentSearchResultsAndAnswer(k=this.__k,
                                               search_results=[])

        # Initialisation de la barre de chargement
        nb_doc = len(dataset.search_results)
        progress_bar = tqdm(total=nb_doc, desc="Answering question")

        # Boucle sur toutes les questions pour y répondre
        try:

            for question in dataset.search_results:

                min_ans = this.__answer_one_question(question)
                answer.search_results.append(min_ans)

                progress_bar.update(1)

        except Exception as e:
            raise Exception(e)

        finally:
            progress_bar.close()

        # Enregistrement des résultats
        res = answer.model_dump_json(indent=2)

        name = os.path.basename(this.__search_path)
        output_file = os.path.join(this.__save_path, name)

        os.makedirs(this.__save_path, exist_ok=True)
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(res)

        print(f"Saved student_search_results_and_answer to "
              f"{this.__save_path}{name}")

    # +---------------------------------------------------------------------+
    # |                           Answer Methods                            |
    # +---------------------------------------------------------------------+

    def __answer_one_question(this,
                              src_res: MinimalSearchResults) -> MinimalAnswer:

        question = src_res

        # Génération du prompt
        start_prompt = this.__init_prompt_sys()
        user_prompt = this.__init_prompt_usr(question)

        # Génération de la réponse
        chat = [
            {"role": "system", "content": start_prompt},
            {"role": "user", "content": user_prompt}
        ]

        response = this.__pipeline(chat, max_new_tokens=500)
        reponse = response[0]["generated_text"][-1]["content"]
        rep = reponse.split("</think>\n\n")

        # Renvoie de la réponse
        min_ans = MinimalAnswer(answer=rep[1],
                                question_id=question.question_id,
                                question_str=question.question_str,
                                retrieved_sources=question.retrieved_sources)

        return min_ans

    # +---------------------------------------------------------------------+
    # |                           Prompt Methods                            |
    # +---------------------------------------------------------------------+

    def __init_prompt_sys(this) -> str:

        start_prompt = ("You are a helpful assistant expert in LLM domain. "
                        "Answer the question using the provided context. "
                        "Be concise and precise. Answer: /no_think")

        return start_prompt

    def __init_prompt_usr(this, shrc_res: MinimalSearchResults) -> str:

        context_parts: list[str] = []

        for chunk in shrc_res.retrieved_sources:
            context_parts.append(f"[Source: {chunk.file_path}]\n{chunk.text}")

        context_text = "\n\n---\n\n".join(context_parts)
        context_text = context_text[:3000]
        context_text = context_text + "(truncated)"
        start_prompt = (f"Contexte: {context_text}\n\n"
                        f"Question : {this.__question}")

        return start_prompt

    # +---------------------------------------------------------------------+
    # |                           Others Methods                            |
    # +---------------------------------------------------------------------+

    def __is_path_init(this, path: str | None) -> bool:

        if (path is not None):
            return os.path.exists(path)
        return True
