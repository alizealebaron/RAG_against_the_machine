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
# @update   : 2026/05/15 10:50:20 by alebaron                                #
# ************************************************************************** #

# +-------------------------------------------------------------------------+
# |                               Importation                               |
# +-------------------------------------------------------------------------+


import os
import json
from tqdm import tqdm
from src.utils.error import exit_error, IndexError
from src.cli_functions.index.chunk import make_chunk_md, make_chunk_py
from src.cli_functions.index.chunk import convert_lst_chunk_to_dict


# +-------------------------------------------------------------------------+
# |                                  Main                                   |
# +-------------------------------------------------------------------------+

def cli_index(max_chunk_size: int):

    directory = "data/raw/vllm-0.10.1/"
    lst_chunk = []
    dict_chunk = {}
    nb_doc = get_nb_doc(directory)
    progress_bar = tqdm(total=nb_doc)

    try:

        for root, dirs, files in os.walk(directory):
            for file in files:

                if (file.endswith(".md") or file.endswith(".py")):

                    path = (os.path.join(root, file))

                    with open(path, "r") as f:
                        content = f.read()

                    if (path.endswith(".md")):
                        lst_chunk = make_chunk_md(content, max_chunk_size)
                        dict_chunk = convert_lst_chunk_to_dict(lst_chunk)
                    elif (path.endswith(".py")):
                        dict_chunk = make_chunk_py(content, max_chunk_size)

                    out_dir = "data/processed/chunks"
                    out_name = file + ".json"

                    os.makedirs(out_dir, exist_ok=True)

                    output_file = os.path.join(out_dir, out_name)
                    with open(output_file, "w") as f:
                        json.dump(dict_chunk, f, indent=2)

                    progress_bar.update(1)

        out_dir = "data/processed/bm25_index"
        os.makedirs(out_dir, exist_ok=True)

    except Exception as e:
        print(e)
        exit_error(IndexError(), e)


def get_nb_doc(path: str) -> int:

    nb_doc = 0

    for root, dirs, files in os.walk(path):
        for file in files:
            if (file.endswith(".md") or file.endswith(".py")):
                nb_doc += 1

    return nb_doc
