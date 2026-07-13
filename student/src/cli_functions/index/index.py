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
# @update   : 2026/07/13 11:19:40 by alebaron                                #
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
from ...utils.error import IndexError, print_error
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

    """
    Class representing the indexing functionality.

    Methods:
        indexing(): Indexes the documents in the specified directory and
            saves the chunks and BM25 index to the specified paths.
    """

    # +---------------------------------------------------------------------+
    # |                                 Init                                |
    # +---------------------------------------------------------------------+

    def __init__(this, max_chunk_size: int):

        """
        Initializes the Index class.

        Args:
            max_chunk_size (int): The maximum size of each chunk.
        """

        this.__max_chunk_size = max_chunk_size
        this.__nb_doc = this.__get_nb_doc(VLLM_PATH)
        this.__lst_chunk: List[Chunk] = []
        this.__last_id = 0

        if (int(max_chunk_size) < 1):
            print_error(IndexError(), "chunk_size value can't be < 1."
                                      "default value will be used (2000).")
            max_chunk_size = 2000

    # +---------------------------------------------------------------------+
    # |                           Indexing Methods                          |
    # +---------------------------------------------------------------------+

    def indexing(this) -> None:

        """
        Indexes the documents in the specified directory and saves the chunks
        and BM25 index to a specified paths.
        """

        # Initialisation de la barre de progression
        progress_bar = tqdm(total=this.__nb_doc, desc="Chunking vllm files")

        # Parcours de tous les fichiers présents dans le dossier sources
        for root, dirs, files in os.walk(VLLM_PATH):

            for file in files:

                tmp_path = (root + "/" + file)[3::]
                if ((file.endswith(".md") or file.endswith(".py"))):

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

        # Variable d'overlap en nombre de caractères
        OVERLAP_SIZE = 150

        # Initialisation des variables
        header_pattern = r"^#{1,5}\s+.+$"
        lines = text.splitlines(True)
        current_chunk: List[str] = []
        current_header = ""
        current_length = 0

        # Initialisation des curseurs
        chunk_start_curseur = 0
        running_curseur = 0

        # Boucle sur toutes les lignes
        for line in lines:

            line_len = len(line)
            is_header = bool(re.match(header_pattern, line.strip()))

            # On coupe un texte en cas de titre ou de ligne trop longue
            if ((is_header or (current_length + line_len >
                               this.__max_chunk_size)) and current_chunk):

                chunk_text = ''.join(current_chunk).strip()

                # Création du chunk
                if chunk_text:
                    this.__add_create_chunk(chunk_text, "md", file_path,
                                            chunk_start_curseur,
                                            running_curseur - 1)

                # Calcul de l'overlap
                overlap_prefix = ""
                if OVERLAP_SIZE > 0:
                    # On extrait les N derniers caractères du texte accumulé
                    full_current_str = ''.join(current_chunk)
                    overlap_prefix = full_current_str[-OVERLAP_SIZE:]

                # Préparation du nouveau chunk avec l'overlap et le header
                current_chunk = []
                current_length = 0

                # On réinjecte l'overlap du chunk précédent s'il existe
                if overlap_prefix:
                    current_chunk.append(overlap_prefix)
                    current_length += len(overlap_prefix)

                # On réinjecte le titre
                if not is_header and current_header:
                    header_line = current_header + "\n"
                    current_chunk.append(header_line)
                    current_length += len(header_line)

                # On ajoute la ligne courante
                current_chunk.append(line)
                current_length += line_len

                # Calcul de l'index de départ corrigé
                chunk_start_curseur = max(0, (running_curseur -
                                              len(overlap_prefix)))

                if is_header:
                    current_header = line.strip()

            # Si la ligne est pas trop grande, on continue
            else:
                if is_header:
                    current_header = line.strip()

                if not current_chunk:
                    chunk_start_curseur = running_curseur

                current_chunk.append(line)
                current_length += line_len

            running_curseur += line_len

        # Traitement du tout dernier chunk
        if current_chunk:
            chunk_text = ''.join(current_chunk).strip()
            if chunk_text:
                this.__add_create_chunk(chunk_text, "md",
                                        file_path,
                                        chunk_start_curseur,
                                        running_curseur - 1)

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

    def __verify_chunk_size(this) -> None:

        i = 0
        for chunk in this.__lst_chunk:
            if (len(chunk.text) > this.__max_chunk_size):
                print(f"{chunk.id} ({chunk.fichier}) too long ! "
                      f"({len(chunk.text)})")
                i += 1

        if (i != 0):
            print(f"Nombre de fichier incorrect: {i}")
