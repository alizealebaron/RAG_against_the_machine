# ************************************************************************** #
#       _  _     ____                     ,~~.                               #
#      | || |   |___  \             ,   (  ^ )>                              #
#      | || |_    __) |             )\~~'   (       _      _      _          #
#      |__   _|  / __/             (  .__)   )    >(.)__ <(^)__ =(o)__       #
#         |_|   |_____| .fr         \_.____,*      (___/  (___/  (___/       #
#                                                                            #
# ************************************************************************** #
# @name   : init_questions.py                                                #
# @author : alebaron <alebaron@student.42lehavre.fr>                         #
#                                                                            #
# @creation : 2026/05/12 10:53:43 by alebaron                                #
# @update   : 2026/05/12 13:10:46 by alebaron                                #
# ************************************************************************** #

# +-------------------------------------------------------------------------+
# |                               Importation                               |
# +-------------------------------------------------------------------------+


from typing import List
from json import JSONDecodeError, load
from src.models.answeredQuestion import AnsweredQuestion
from src.models.unansweredQuestion import UnansweredQuestion
from src.utils.error import exit_error, FileError


# +-------------------------------------------------------------------------+
# |                                 Methods                                 |
# +-------------------------------------------------------------------------+

def get_lst_answered_questions():

    lst_ans = List[AnsweredQuestion]

    try:
        with open("data/datasets/AnsweredQuestions/dataset_code_public.json", "r") as file:
            data = load(file)
            lst_ans = [AnsweredQuestion(**arg) for arg in data["rag_questions"]]

        with open("data/datasets/AnsweredQuestions/dataset_docs_public.json", "r") as file:
            data = load(file)
            lst_tmp = [AnsweredQuestion(**arg) for arg in data["rag_questions"]]
            lst_ans += lst_tmp

    except JSONDecodeError as e:
        exit_error(FileError(), f"Invalid JSON syntax at "
                   f"line {e.lineno}.")

    except Exception as e:
        exit_error(FileError(), str(e))

    return (lst_ans)


def get_lst_unanswered_questions():

    lst_unans = List[UnansweredQuestion]

    try:
        with open("data/datasets/UnansweredQuestions/dataset_docs_public.json", "r") as file:
            data = load(file)
            lst_unans = [UnansweredQuestion(**arg) for arg in data["rag_questions"]]

        with open("data/datasets/UnansweredQuestions/dataset_code_public.json", "r") as file:
            data = load(file)
            lst_tmp = [UnansweredQuestion(**arg) for arg in data["rag_questions"]]
            lst_unans += lst_tmp

    except JSONDecodeError as e:
        exit_error(FileError(), f"Invalid JSON syntax at "
                   f"line {e.lineno}.")

    except Exception as e:
        exit_error(FileError(), str(e))

    return (lst_unans)
