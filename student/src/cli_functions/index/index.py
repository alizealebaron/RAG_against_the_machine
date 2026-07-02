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
# @update   : 2026/07/02 15:10:21 by alebaron                                #
# ************************************************************************** #

# +-------------------------------------------------------------------------+
# |                              Importation                                |
# +-------------------------------------------------------------------------+

import os
import json
import bm25s
from tqdm import tqdm
from typing import List
from ...models.models import Chunk
from ...utils.error import exit_error, IndexError, print_error
from ..index.chunk import make_chunk_md, make_chunk_py
from ..index.chunk import convert_lst_chunk_for_json

# +-------------------------------------------------------------------------+
# |                              Importation                                |
# +-------------------------------------------------------------------------+


DATA_PATH = "../data"
BM25_PATH = f"{DATA_PATH}/processed/bm25_index"


# +-------------------------------------------------------------------------+
# |                                Methods                                  |
# +-------------------------------------------------------------------------+

def cli_index(max_chunk_size: int):

    if (max_chunk_size < 1):
        print_error(IndexError(), "chunk_size value can't be < 1."
                                  "default value will be used (2000).")
        max_chunk_size = 2000

    directory = f"{DATA_PATH}/vllm-0.10.1/"
    # directory = f"{DATA_PATH}/test_datasets"
    lst_chunk = []
    nb_doc = get_nb_doc(directory)
    lst_id = 0

    try:

        max_chunk_size = int(max_chunk_size)
        progress_bar = tqdm(total=nb_doc, desc="Chunking vllm files")

        for root, dirs, files in os.walk(directory):
            for file in files:

                tmp_path = (root + "/" + file)[3::]

                if (file.endswith(".md") or file.endswith(".py")):

                    path = (os.path.join(root, file))

                    with open(path, "r") as f:
                        content = f.read()

                    if (path.endswith(".md")):
                        tmp_lst = make_chunk_md(content, max_chunk_size,
                                                lst_id, tmp_path)
                        lst_chunk.extend(convert_lst_chunk_for_json(tmp_lst))
                    elif (path.endswith(".py")):
                        tmp_lst = make_chunk_py(content, max_chunk_size,
                                                lst_id, tmp_path)
                        lst_chunk.extend(convert_lst_chunk_for_json(tmp_lst))

                    lst_id = (lst_chunk[-1]['id'] + 1)

                    progress_bar.update(1)

        # Coupe des textes trop gros en .md
        for chunk in lst_chunk:
            if (chunk['fichier'] == "md" and
               len(chunk["text"]) > max_chunk_size):
                chunk["text"] = chunk["text"][0:max_chunk_size]

        # Sauvegarde de l'indexage des documents

        corpus_texts = [chunk["text"] for chunk in lst_chunk]
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
            json.dump(lst_chunk, f, indent=2)

        verify_chunk_size(max_chunk_size, lst_chunk)

    except Exception as e:
        exit_error(IndexError(), e)

    finally:
        progress_bar.close()


def get_nb_doc(path: str) -> int:

    nb_doc = 0

    for root, dirs, files in os.walk(path):
        for file in files:
            if (file.endswith(".md") or file.endswith(".py")):
                nb_doc += 1

    return nb_doc


def verify_chunk_size(max_chunk_size: int, lst_chunk: List[Chunk]):

    i = 0
    for chunk in lst_chunk:
        if (len(chunk["text"]) > max_chunk_size):
            # if (chunk['fichier'] == "md"):
            #     print(len(chunk['text']))
            print(f"{chunk['id']} ({chunk['fichier']}) too long ! "
                  f"({len(chunk['text'])})")
            i += 1

    print(f"Nombre de fichier incorrect: {i}")
