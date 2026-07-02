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
# @update   : 2026/07/02 16:45:57 by alebaron                                #
# ************************************************************************** #

# +-------------------------------------------------------------------------+
# |                              Importation                                |
# +-------------------------------------------------------------------------+


import os
from ...utils.error import EvaluateError, print_error


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
        pass

    # +---------------------------------------------------------------------+
    # |                           Others Methods                            |
    # +---------------------------------------------------------------------+

    def __is_path_init(this, path: str) -> bool:

        return os.path.exists(path)
