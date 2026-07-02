# ************************************************************************** #
#       _  _     ____                     ,~~.                               #
#      | || |   |___  \             ,   (  ^ )>                              #
#      | || |_    __) |             )\~~'   (       _      _      _          #
#      |__   _|  / __/             (  .__)   )    >(.)__ <(^)__ =(o)__       #
#         |_|   |_____| .fr         \_.____,*      (___/  (___/  (___/       #
#                                                                            #
# ************************************************************************** #
# @name   : __main__.py                                                      #
# @author : alebaron <alebaron@student.42lehavre.fr>                         #
#                                                                            #
# @creation : 2026/05/07 11:47:53 by alebaron                                #
# @update   : 2026/07/02 14:55:35 by alebaron                                #
# ************************************************************************** #

# +-------------------------------------------------------------------------+
# |                               Importation                               |
# +-------------------------------------------------------------------------+


# try:
import sys
import fire
from .cli_functions.index.index import cli_index
from .cli_functions.search.search import Search
from .cli_functions.answer.answer import Answer
from .cli_functions.evaluate.evaluate import Evaluation
from .utils.error import SearchError, exit_error, AnswerError
# except Exception:
#     print("ImportationError: Some package are not present. Please do "
#           "`uv sync` to install a python env.")
#     sys.exit(2)


# +-------------------------------------------------------------------------+
# |                                 Classe                                  |
# +-------------------------------------------------------------------------+

def index(max_chunk_size=2000):

    cli_index(max_chunk_size)
    print("Ingestion complete! Indices saved under data/processed/")


def search(question: str, k=10):

    print(" Begin of search ".center(70, "~"))

    try:
        search = Search(question=question, k=k)
        result = search.search_single()
        result = result.model_dump_json(indent=2)
        print(result)

    except Exception as e:
        exit_error(SearchError(), e)

    print(" Search completed ! ".center(70, "~") + "\n")


def search_dataset(dataset_path: str, save_directory: str, k=10) -> None:

    print(" Begin of search ".center(70, "~"))

    try:
        search = Search(k=k, dataset_path=dataset_path,
                        save_path=save_directory)
        search.search_dataset()

    except Exception as e:
        exit_error(SearchError(), e)

    finally:
        print(" Search completed ! ".center(70, "~") + "\n")


def answer(question: str, k=10):

    print(" Begin of answer ".center(70, "~"))

    try:
        answer = Answer(k, question=question)
        result = answer.answer_single()
        result = result.model_dump_json(indent=2)
        print(result)
    except Exception as e:
        exit_error(AnswerError(), e)
    finally:
        print(" Answer completed ! ".center(70, "~") + "\n")


def answer_dataset(student_search_results_path: str,
                   save_directory: str, k=10):

    print(" Begin of answer ".center(70, "~"))

    try:

        ans = Answer(k, search_path=student_search_results_path,
                     save_path=save_directory)
        ans.answer_dataset()

    except Exception as e:
        exit_error(AnswerError(), e)

    finally:
        print(" Answer completed ! ".center(70, "~") + "\n")


def evaluate(student_answer_path: str, dataset_path: str,
             k=10, max_context_length=2000):

    print(" Begin of evaluation ".center(70, "~"))

    try:
        eval = Evaluation(student_answer_path, dataset_path,
                          k, max_context_length)

    except Exception as e:
        exit_error(AnswerError(), e)

    finally:
        print(" Evaluation completed ! ".center(70, "~") + "\n")


# +-------------------------------------------------------------------------+
# |                                  Main                                   |
# +-------------------------------------------------------------------------+

if __name__ == '__main__':

    try:
        fire.Fire()
    except Exception as e:
        print(e)
    # fire.Fire()
