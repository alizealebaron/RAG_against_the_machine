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
# @update   : 2026/07/01 13:24:49 by alebaron                                #
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

    # +---------------------------------------------------------------------+
    # |                            Attributs                                |
    # +---------------------------------------------------------------------+

    question_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    question: str


class MinimalSource(BaseModel):

    # +---------------------------------------------------------------------+
    # |                            Attributs                                |
    # +---------------------------------------------------------------------+

    file_path: str
    first_character_index: int
    last_character_index: int


class MinimalSearchResults(BaseModel):

    # +---------------------------------------------------------------------+
    # |                            Attributs                                |
    # +---------------------------------------------------------------------+

    question_id: str
    question_str: str
    retrieved_sources: List[MinimalSource]


class StudentSearchResults(BaseModel):

    # +---------------------------------------------------------------------+
    # |                            Attributs                                |
    # +---------------------------------------------------------------------+

    search_results: List[MinimalSearchResults]
    k: int


class MinimalAnswer(MinimalSearchResults):

    # +---------------------------------------------------------------------+
    # |                            Attributs                                |
    # +---------------------------------------------------------------------+

    answer: str


class StudentSearchResultsAndAnswer(StudentSearchResults):

    # +---------------------------------------------------------------------+
    # |                            Attributs                                |
    # +---------------------------------------------------------------------+

    search_results: List[MinimalAnswer]
    k: int


class AnsweredQuestion(UnansweredQuestion):

    # +---------------------------------------------------------------------+
    # |                            Attributs                                |
    # +---------------------------------------------------------------------+

    sources: List[MinimalSource]
    answer: str
    difficulty: str
    is_valid: bool


class RagDataset(BaseModel):

    # +---------------------------------------------------------------------+
    # |                            Attributs                                |
    # +---------------------------------------------------------------------+

    rag_questions: List[AnsweredQuestion | UnansweredQuestion]


class Chunk(MinimalSource):

    # +---------------------------------------------------------------------+
    # |                            Attributs                                |
    # +---------------------------------------------------------------------+

    id: int
    text: str
    fichier: str
