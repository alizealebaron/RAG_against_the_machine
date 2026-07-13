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
# @update   : 2026/07/13 11:17:45 by alebaron                                #
# ************************************************************************** #

# +-------------------------------------------------------------------------+
# |                               Importation                               |
# +-------------------------------------------------------------------------+


try:
    import sys
    import fire
    from .cli_functions.index.index import Index
    from .cli_functions.search.search import Search
    from .cli_functions.answer.answer import Answer
    from .cli_functions.evaluate.evaluate import Evaluation
    from .utils.error import SearchError, exit_error, AnswerError
    from .utils.error import EvaluateError
    from .utils.error import IndexError
except Exception:
    print("ImportationError: Some package are not present. Please do "
          "`uv sync` to install a python env.")
    sys.exit(2)


# +-------------------------------------------------------------------------+
# |                                 Classe                                  |
# +-------------------------------------------------------------------------+

def index(max_chunk_size: int = 2000) -> None:

    """
    Function to index the data and create the BM25 index.

    Args:
        max_chunk_size (int): The maximum size of each chunk. Default is 2000.
    """

    try:
        index = Index(max_chunk_size)
        index.indexing()

    except Exception as e:
        exit_error(IndexError(), e)

    print("Ingestion complete! Indices saved under data/processed/")


def search(question: str, k: int = 10) -> None:

    """
    Function to search for the most relevant chunks based on a question.

    Args:
        question (str): The question to search for.
        k (int): The number of top results to return. Default is 10.
    """

    print(" Begin of search ".center(70, "~"))

    try:
        search = Search(question=question, k=k)
        result = search.search_single()
        result = result.model_dump_json(indent=2)
        print(result)

    except Exception as e:
        exit_error(SearchError(), e)

    print(" Search completed ! ".center(70, "~") + "\n")


def search_dataset(dataset_path: str,
                   save_directory: str,
                   k: int = 10) -> None:

    """
    Function to search for the most relevant chunks based on a dataset.

    Args:
        dataset_path (str): The path to the dataset to search.
        save_directory (str): The directory to save the search results.
        k (int): The number of top results to return. Default is 10.
    """

    print(" Begin of search ".center(70, "~"))

    try:
        search = Search(
            k=k,
            dataset_path=dataset_path,
            save_path=save_directory,
        )
        search.search_dataset()

    except Exception as e:
        exit_error(SearchError(), e)

    finally:
        print(" Search completed ! ".center(70, "~") + "\n")


def answer(question: str, k: int = 10) -> None:

    """
    Function to answer a question based on the most relevant chunks.

    Args:
        question (str): The question to answer.
        k (int): The number of top results for answering. Default is 10.
    """

    print(" Begin of answer ".center(70, "~"))

    try:
        answer = Answer(k, question=question)
        result = answer.answer_single()
        answer_text = result.search_results[0].answer
        print(answer_text)
    except Exception as e:
        exit_error(AnswerError(), e)
    finally:
        print(" Answer completed ! ".center(70, "~") + "\n")


def answer_dataset(student_search_results_path: str,
                   save_directory: str, k: int = 10) -> None:

    """
    Function to answer questions based on a dataset of search results.

    Args:
        student_search_results_path (str): The path to the dataset of search
            results.
        save_directory (str): The directory to save the answers.
        k (int): The number of top results for answering. Default is 10.
    """

    print(" Begin of answer ".center(70, "~"))

    try:

        ans = Answer(k, search_path=student_search_results_path,
                     save_path=save_directory)
        ans.answer_dataset()

    except Exception as e:
        exit_error(AnswerError(), e)

    finally:
        print(" Answer completed ! ".center(70, "~") + "\n")


def evaluate(student_answer_path: str,
             dataset_path: str,
             k: int = 10,
             max_context_length: int = 2000) -> None:

    """
    Function to evaluate the answers based on a dataset of search results.

    Args:
        student_answer_path (str): The path to the dataset of answers.
        dataset_path (str): The path to the dataset to evaluate against.
        k (int): The number of top results for evaluation. Default is 10.
        max_context_length (int): The maximum length of context to consider
            for evaluation. Default is 2000.
    """

    print(" Begin of evaluation ".center(70, "~"))

    try:
        eval = Evaluation(student_answer_path, dataset_path,
                          k, max_context_length)
        eval.evaluate()

    except Exception as e:
        exit_error(EvaluateError(), e)

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
