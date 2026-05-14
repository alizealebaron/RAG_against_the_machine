# ************************************************************************** #
#       _  _     ____                     ,~~.                               #
#      | || |   |___  \             ,   (  ^ )>                              #
#      | || |_    __) |             )\~~'   (       _      _      _          #
#      |__   _|  / __/             (  .__)   )    >(.)__ <(^)__ =(o)__       #
#         |_|   |_____| .fr         \_.____,*      (___/  (___/  (___/       #
#                                                                            #
# ************************************************************************** #
# @name   : chunk.py                                                         #
# @author : alebaron <alebaron@student.42lehavre.fr>                         #
#                                                                            #
# @creation : 2026/05/12 15:21:04 by alebaron                                #
# @update   : 2026/05/14 15:19:32 by alebaron                                #
# ************************************************************************** #

# +-------------------------------------------------------------------------+
# |                               Importation                               |
# +-------------------------------------------------------------------------+


import re
from typing import Any
from astchunk import ASTChunkBuilder


# +-------------------------------------------------------------------------+
# |                                  Main                                   |
# +-------------------------------------------------------------------------+

def make_chunk_md(text: str, chunk_max_size: int) -> list[str]:

    header_pattern = r"^#{1,3}\s+.+$"
    lines = text.split('\n')
    chunks = []
    current_chunk = []
    current_header = ""
    current_length = 0

    for line in lines:
        # Détection d'un titre
        if re.match(header_pattern, line, re.MULTILINE):
            # Sauvegarder le chunk précédent
            if current_chunk:
                chunk_text = '\n'.join(current_chunk).strip()
                if chunk_text:
                    chunks.append(chunk_text)

            current_header = line
            current_chunk = [line]
            current_length = len(line)
        else:
            # Vérifier la limite de taille
            if current_length + len(line) > chunk_max_size and current_chunk:
                chunk_text = '\n'.join(current_chunk).strip()
                if chunk_text:
                    chunks.append(chunk_text)
                # Nouveau chunk avec le header pour le contexte
                current_chunk = [current_header, line] if current_header else [line]
                current_length = len(current_header) + len(line)
            else:
                current_chunk.append(line)
                current_length += len(line) + 1

    # Dernier chunk
    if current_chunk:
        chunk_text = '\n'.join(current_chunk).strip()
        if chunk_text:
            chunks.append(chunk_text)

    return chunks


def make_chunk_py(text: str, chunk_max_size: int) -> dict[str, str]:

    dict_chunk = {}

    # Initialize the chunk builder
    configs = {
        "max_chunk_size": chunk_max_size,
        "language": "python",
        "metadata_template": "default"
    }

    chunk_builder = ASTChunkBuilder(**configs)
    chunks = chunk_builder.chunkify(text)

    for i, chunk in enumerate(chunks):
        dict_chunk[f"chunk_{i}"] = chunk['content']

    return dict_chunk


def convert_lst_chunk_to_dict(lst_chunk: list[str]) -> dict[Any, Any]:

    dict_chunk = {}

    i = 0
    for chunk in lst_chunk:

        dict_chunk[f"chunk_{i}"] = chunk
        i += 1

    return (dict_chunk)
