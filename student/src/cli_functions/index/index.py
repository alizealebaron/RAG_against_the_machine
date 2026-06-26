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
# @update   : 2026/06/26 13:22:10 by alebaron                                #
# ************************************************************************** #

# +-------------------------------------------------------------------------+
# |                              Importation                                |
# +-------------------------------------------------------------------------+

import os
import json
from tqdm import tqdm
from ...utils.error import exit_error, IndexError
from ..index.chunk import make_chunk_md, make_chunk_py
from ..index.chunk import convert_lst_chunk_for_json

# +-------------------------------------------------------------------------+
# |                              Importation                                |
# +-------------------------------------------------------------------------+


DATA_PATH = "../data"


# +-------------------------------------------------------------------------+
# |                                Methods                                  |
# +-------------------------------------------------------------------------+

def cli_index(max_chunk_size: int):

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

        out_dir = f"{DATA_PATH}/processed/chunks/"
        out_name = "chunk.json"

        os.makedirs(out_dir, exist_ok=True)

        output_file = os.path.join(out_dir, out_name)
        with open(output_file, "w") as f:
            json.dump(lst_chunk, f, indent=2)

        out_dir = f"{DATA_PATH}/processed/bm25_index"
        os.makedirs(out_dir, exist_ok=True)

    except Exception as e:
        exit_error(IndexError(), e)


def get_nb_doc(path: str) -> int:

    nb_doc = 0

    for root, dirs, files in os.walk(path):
        for file in files:
            if (file.endswith(".md") or file.endswith(".py")):
                nb_doc += 1

    return nb_doc
