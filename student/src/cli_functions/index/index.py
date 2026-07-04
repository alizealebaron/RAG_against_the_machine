# ************************************************************************** #
#       _  _     ____                     ,~~.                               #
#      | || |   |___  \             ,   (  ^ )>                              #
#      | || |_    __) |             )\~~'   (       _      _      _          #
#      |__   _|  / __/             (  .__)   )    >(.)__ <(^)__ =(o)__       #
#         |_|   |_____| .fr         \_.____,*      (___/  (___/  (___/       #
#                                                                            #
# ************************************************************************** #
# @name   : index.py                                                         #
# @author : alebaron <alebaron@student.42lehavre.fr>                         #
#                                                                            #
# @creation : 2026/05/07 15:11:09 by alebaron                                #
# @update   : 2026/07/04 17:45:12 by alebaron                                #
# ************************************************************************** #

# +-------------------------------------------------------------------------+
# |                              Importation                                |
# +-------------------------------------------------------------------------+

import os
import re
import json
import bm25s
from tqdm import tqdm
from typing import List
from ...models.models import Chunk
from ...utils.error import exit_error, IndexError, print_error
from ..index.chunk import convert_lst_chunk_for_json
from astchunk import ASTChunkBuilder
from langchain_text_splitters import RecursiveCharacterTextSplitter

# +-------------------------------------------------------------------------+
# |                              Importation                                |
# +-------------------------------------------------------------------------+


DATA_PATH = "../data"
VLLM_PATH = f"{DATA_PATH}/raw/vllm-0.10.1/"
BM25_PATH = f"{DATA_PATH}/processed/bm25_index"


# +-------------------------------------------------------------------------+
# |                                 Classe                                  |
# +-------------------------------------------------------------------------+

class Index():

    # +---------------------------------------------------------------------+
    # |                                 Init                                |
    # +---------------------------------------------------------------------+

    def __init__(this, max_chunk_size: int):

        this.__max_chunk_size = max_chunk_size
        this.__nb_doc = this.__get_nb_doc(VLLM_PATH)
        this.__lst_chunk = []
        this.__last_id = 0

        if (int(max_chunk_size) < 1):
            print_error(IndexError(), "chunk_size value can't be < 1."
                                      "default value will be used (2000).")
            max_chunk_size = 2000

    # +---------------------------------------------------------------------+
    # |                           Indexing Methods                          |
    # +---------------------------------------------------------------------+

    def indexing(this):

        # Initialisation de la barre de progression
        progress_bar = tqdm(total=this.__nb_doc, desc="Chunking vllm files")

        # Parcours de tous les fichiers présents dans le dossier sources
        for root, dirs, files in os.walk(VLLM_PATH):

            for file in files:

                tmp_path = (root + "/" + file)[3::]
                if (file.endswith(".md") or file.endswith(".py")):

                    path = (os.path.join(root, file))

                    # Récupération du contenu du fichier
                    with open(path, "r") as f:
                        content = f.read()

                    # # Chunking des fichiers md
                    if (path.endswith(".md")):
                        this.__make_chunk_md(content, tmp_path)

                    # Chunking des fichiers py
                    if (path.endswith(".py")):
                        this.__make_chunk_py(content, tmp_path)

                    progress_bar.update(1)

        # Sauvegarde de l'indexage des documents
        corpus_texts = [chunk.text for chunk in this.__lst_chunk]
        corpus_tokens = bm25s.tokenize(corpus_texts)
        retriever = bm25s.BM25(corpus=corpus_texts, method="bm25+")
        retriever.index(corpus_tokens)
        retriever.save(BM25_PATH)

        # Sauvegarde des chunks dans un fichier
        out_dir = f"{DATA_PATH}/processed/chunks/"
        out_name = "chunk.json"
        os.makedirs(out_dir, exist_ok=True)

        output_file = os.path.join(out_dir, out_name)
        with open(output_file, "w") as f:
            raw_chunks = [chunk.model_dump() for chunk in this.__lst_chunk]
            json.dump(raw_chunks, f, indent=2, ensure_ascii=False)

        # Vérification de la taille des chunks
        this.__verify_chunk_size()

    # +---------------------------------------------------------------------+
    # |                           Chunking Methods                          |
    # +---------------------------------------------------------------------+

    def __make_chunk_md(this, text: str, file_path: str) -> None:

        

    def __make_chunk_py(this, text: str, file_path: str) -> None:

        # Initialisation des variables
        last_index = 0

        # Initialize the chunk builder
        configs = {
            "max_chunk_size": this.__max_chunk_size,
            "language": "python",
            "metadata_template": "default"
        }

        chunk_builder = ASTChunkBuilder(**configs)
        chunks = chunk_builder.chunkify(text)

        fallback_splitter = RecursiveCharacterTextSplitter.from_language(
            language="python",
            chunk_size=this.__max_chunk_size,
            chunk_overlap=150
        )

        # Parcours de tous les chunks découpés
        for chunk in chunks:

            content = chunk['content']

            # Si le chunk respecte la taille, on l'ajoute normalement
            if len(content) <= this.__max_chunk_size:
                sub_contents = [content]
            # Sinon, on force le sous-découpage du gros bloc
            else:
                sub_contents = fallback_splitter.split_text(content)

            # Récupération de tous les sous chunk pour les transformer
            for sub_content in sub_contents:
                this.__add_create_chunk(
                    sub_content,
                    "py",
                    file_path,
                    last_index,
                    last_index + len(sub_content) - 1
                )
                last_index += len(sub_content) + 1

    # +---------------------------------------------------------------------+
    # |                            Create Chunk                             |
    # +---------------------------------------------------------------------+

    def __add_create_chunk(this, text: str, fichier: str, file_path: str,
                           first_i: int, last_i: int) -> None:

        dict_tmp = {
            "id": this.__last_id,
            "text": text,
            "fichier": fichier,
            "file_path": file_path,
            "first_character_index": first_i,
            "last_character_index": last_i
        }

        chunk_tmp = Chunk(**dict_tmp)

        this.__last_id += 1
        this.__lst_chunk.append(chunk_tmp)

    # +---------------------------------------------------------------------+
    # |                            Small Methods                            |
    # +---------------------------------------------------------------------+

    def __get_nb_doc(this, path: str) -> int:

        nb_doc = 0

        for root, dirs, files in os.walk(path):
            for file in files:
                if (file.endswith(".md") or file.endswith(".py")):
                    nb_doc += 1

        return nb_doc

    def __verify_chunk_size(this):

        i = 0
        for chunk in this.__lst_chunk:
            if (len(chunk.text) > this.__max_chunk_size):
                print(f"{chunk['id']} ({chunk['fichier']}) too long ! "
                      f"({len(chunk['text'])})")
                i += 1

        print(f"Nombre de fichier incorrect: {i}")
