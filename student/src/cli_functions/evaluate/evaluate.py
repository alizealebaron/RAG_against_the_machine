# ************************************************************************** #
#       _  _     ____                     ,~~.                               #
#      | || |   |___  \             ,   (  ^ )>                              #
#      | || |_    __) |             )\~~'   (       _      _      _          #
#      |__   _|  / __/             (  .__)   )    >(.)__ <(^)__ =(o)__       #
#         |_|   |_____| .fr         \_.____,*      (___/  (___/  (___/       #
#                                                                            #
# ************************************************************************** #
# @name   : evaluate.py                                                      #
# @author : alebaron <alebaron@student.42lehavre.fr>                         #
#                                                                            #
# @creation : 2026/07/02 14:52:01 by alebaron                                #
# @update   : 2026/07/04 11:18:33 by alebaron                                #
# ************************************************************************** #

# +-------------------------------------------------------------------------+
# |                              Importation                                |
# +-------------------------------------------------------------------------+


import os
import json
from typing import List
from ...utils.error import EvaluateError, print_error
from ...models.models import AnsweredQuestion, MinimalSearchResults, Chunk
from ...models.models import StudentSearchResults


# +-------------------------------------------------------------------------+
# |                                 Class                                   |
# +-------------------------------------------------------------------------+

class Evaluation():

    # +---------------------------------------------------------------------+
    # |                                 Init                                |
    # +---------------------------------------------------------------------+

    def __init__(this, student_answer_path: str, dataset_path: str,
                 k: int, max_context_length: int):

        # Initialisation des valeurs
        this.__student_answer_path = student_answer_path
        this.__dataset_path = dataset_path
        this.__k = k
        this.__max_context_length = max_context_length

        # Vérification des chemins
        if (this.__is_path_init(this.__student_answer_path) is False):
            raise EvaluateError(f"Cannot find {this.__student_answer_path}.")

        if (this.__is_path_init(this.__dataset_path) is False):
            raise EvaluateError(f"Cannot find {this.__dataset_path}.")

        # Vérification des valeurs
        if (int(this.__k) < 1):
            print_error(EvaluateError(), f"k value can't be < 1({k})."
                                         "default value will be used (5).")
            this.__k = 5

        if (int(this.__max_context_length) < 1):
            print_error(EvaluateError(), f"max_context_length value can't be"
                                         f" < 1 ({this.__max_context_length})."
                                         "default value will be used (2000).")
            this.__max_context_length = 2000

    # +---------------------------------------------------------------------+
    # |                            Eval Methods                             |
    # +---------------------------------------------------------------------+

    def evaluate(this) -> None:

        # Initialisation des variables
        lst_ans_chunk = this.__get_cmp_text()
        lst_student_search = this.__get_student_src()
        print("Student data is valid: True")
        nb_sources = len(lst_ans_chunk)
        print(f"Total number of questions: {nb_sources}")
        print(f"Total number of questions with sources: {nb_sources}")
        print(f"Total number of questions with student sources:"
              f" {len(lst_student_search)}")

        recall1 = this.__recallk(lst_ans_chunk, lst_student_search, 1)
        recall3 = this.__recallk(lst_ans_chunk, lst_student_search, 3)
        recall5 = this.__recallk(lst_ans_chunk, lst_student_search, 5)
        recall10 = this.__recallk(lst_ans_chunk, lst_student_search, 10)

        # Affichage des résultats
        print("Evaluation Results")
        print("========================================")
        print(f"Questions evaluated: {nb_sources}")
        print(f"Recall@1: {(recall1 / nb_sources):.3f}")
        print(f"Recall@3: {(recall3 / nb_sources):.3f}")
        print(f"Recall@5: {(recall5 / nb_sources):.3f}")
        print(f"Recall@10: {(recall10 / nb_sources):.3f}")

    # +---------------------------------------------------------------------+
    # |                           Recall@k Methods                          |
    # +---------------------------------------------------------------------+

    def __recallk(this, lst_ans_chunk: List[str],
                  lst_student_search: List[Chunk], k: int) -> int:

        marge_error = 0.05
        nb_positiv = 0

        # Parcours et comparaisons des chunk
        j = 0
        for correct_chunk in lst_ans_chunk:

            words_correct = set(correct_chunk.lower().split())

            if not words_correct:
                continue

            is_valid = False
            for i in range(k):

                chunk = lst_student_search[j].retrieved_sources[i]
                words_student = set(chunk.text.lower().split())

                # Calcul de l'intersection (les mots en commun)
                intersection = words_correct.intersection(words_student)
                overlap_percentage = len(intersection) / len(words_correct)

                if overlap_percentage > marge_error:
                    is_valid = True
                    break

            if is_valid:
                nb_positiv += 1

            j += 1

        return nb_positiv

    # +---------------------------------------------------------------------+
    # |                          Retreiver Methods                          |
    # +---------------------------------------------------------------------+

    def __get_student_src(this) -> List[MinimalSearchResults]:

        with open(this.__student_answer_path, "r") as file:
            data = json.load(file)
        dataset = StudentSearchResults(**data).search_results

        return dataset

    def __get_cmp_text(this) -> List[str]:

        # Récupération du dataset et des questions
        with open(this.__dataset_path, "r") as file:
            data = json.load(file)
        dataset = [AnsweredQuestion(**arg) for arg in data["rag_questions"]]

        # Initialisation de la variable de retour
        lst_check_src = []

        # Boucle sur toutes les questions
        for question in dataset:

            source = question.sources[0]
            try:
                with open(source.file_path, "r") as f:
                    content = f.read()
                text = content[
                    source.first_character_index:source.last_character_index]
                lst_check_src.append(text)

            except Exception:

                with open("../" + source.file_path, "r") as f:
                    content = f.read()
                text = content[
                    source.first_character_index:source.last_character_index]
                lst_check_src.append(text)

        return lst_check_src

    # +---------------------------------------------------------------------+
    # |                           Others Methods                            |
    # +---------------------------------------------------------------------+

    def __is_path_init(this, path: str) -> bool:

        return os.path.exists(path)
