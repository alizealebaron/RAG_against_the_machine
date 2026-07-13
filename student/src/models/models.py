# ************************************************************************** #
#       _  _     ____                     ,~~.                               #
#      | || |   |___  \             ,   (  ^ )>                              #
#      | || |_    __) |             )\~~'   (       _      _      _          #
#      |__   _|  / __/             (  .__)   )    >(.)__ <(^)__ =(o)__       #
#         |_|   |_____| .fr         \_.____,*      (___/  (___/  (___/       #
#                                                                            #
# ************************************************************************** #
# @name   : models.py                                                        #
# @author : alebaron <alebaron@student.42lehavre.fr>                         #
#                                                                            #
# @creation : 2026/06/23 14:18:48 by alebaron                                #
# @update   : 2026/07/13 11:13:26 by alebaron                                #
# ************************************************************************** #

# +-------------------------------------------------------------------------+
# |                               Importation                               |
# +-------------------------------------------------------------------------+


import uuid
from typing import List
from pydantic import BaseModel, Field


# +-------------------------------------------------------------------------+
# |                                 Classe                                  |
# +-------------------------------------------------------------------------+

class UnansweredQuestion(BaseModel):

    """
    Class representing an unanswered question.

    Attributes:
        question_id (str): A unique identifier for the question.
        question (str): The text of the question.
    """

    # +---------------------------------------------------------------------+
    # |                            Attributs                                |
    # +---------------------------------------------------------------------+

    question_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    question: str


class MinimalSource(BaseModel):

    """
    Class representing a minimal source.

    Attributes:
        file_path (str): The path to the source file.
        first_character_index (int): The index of the first character
            in the source.
        last_character_index (int): The index of the last character
            in the source.
    """

    # +---------------------------------------------------------------------+
    # |                            Attributs                                |
    # +---------------------------------------------------------------------+

    file_path: str
    first_character_index: int
    last_character_index: int


class Chunk(MinimalSource):

    """
    Class representing a chunk of text.

    Attributes:
        id (int): A unique identifier for the chunk.
        text (str): The text of the chunk.
        fichier (str): The name of the file from which the chunk was extracted.
    """

    # +---------------------------------------------------------------------+
    # |                            Attributs                                |
    # +---------------------------------------------------------------------+

    id: int
    text: str
    fichier: str


class MinimalSearchResults(BaseModel):

    """
    Class representing minimal search results.

    Attributes:
        question_id (str): A unique identifier for the question.
        question_str (str): The text of the question.
        retrieved_sources (List[Chunk]): A list of retrieved chunks
            that are relevant to the question.
    """

    # +---------------------------------------------------------------------+
    # |                            Attributs                                |
    # +---------------------------------------------------------------------+

    question_id: str
    question_str: str
    retrieved_sources: List[Chunk]


class StudentSearchResults(BaseModel):

    """
    Class representing student search results.

    Attributes:
        search_results (List[MinimalSearchResults]): A list of minimal
            search results.
        k (int): The number of top results to return.
    """

    # +---------------------------------------------------------------------+
    # |                            Attributs                                |
    # +---------------------------------------------------------------------+

    search_results: List[MinimalSearchResults]
    k: int


class MinimalAnswer(MinimalSearchResults):

    """
    Class representing a minimal answer.

    Attributes:
        answer (str): The answer to the question.
    """

    # +---------------------------------------------------------------------+
    # |                            Attributs                                |
    # +---------------------------------------------------------------------+

    answer: str


class StudentSearchResultsAndAnswer(StudentSearchResults):

    """
    Class representing student search results and an answer.

    Attributes:
        search_results (List[MinimalAnswer]): A list of minimal answers.
        k (int): The number of top results to return.
    """

    # +---------------------------------------------------------------------+
    # |                            Attributs                                |
    # +---------------------------------------------------------------------+

    search_results: List[MinimalAnswer]
    k: int


class AnsweredQuestion(UnansweredQuestion):

    """
    Class representing an answered question.

    Attributes:
        sources (List[MinimalSource]): A list of sources used to answer
            the question.
        answer (str): The answer to the question.
        difficulty (str): The difficulty level of the question.
        is_valid (bool): A flag indicating whether the answer is valid.
    """

    # +---------------------------------------------------------------------+
    # |                            Attributs                                |
    # +---------------------------------------------------------------------+

    sources: List[MinimalSource]
    answer: str
    difficulty: str
    is_valid: bool


class RagDataset(BaseModel):

    """
    Class representing a RAG dataset.

    Attributes:
        rag_questions (List[AnsweredQuestion | UnansweredQuestion]): A list of
            answered or unanswered questions in the dataset.
    """

    # +---------------------------------------------------------------------+
    # |                            Attributs                                |
    # +---------------------------------------------------------------------+

    rag_questions: List[AnsweredQuestion | UnansweredQuestion]
