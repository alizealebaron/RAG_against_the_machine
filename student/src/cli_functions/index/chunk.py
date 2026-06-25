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
# @update   : 2026/06/25 18:48:42 by alebaron                                #
# ************************************************************************** #

# +-------------------------------------------------------------------------+
# |                              Importation                                |
# +-------------------------------------------------------------------------+


import re
from typing import Any
from astchunk import ASTChunkBuilder
from ...models.models import Chunk


# +-------------------------------------------------------------------------+
# |                                Methods                                  |
# +-------------------------------------------------------------------------+

def make_chunk_md(text: str, chunk_max_size: int,
                  last_id: int, file_path: str) -> list[Chunk]:

    header_pattern = r"^#{1,3}\s+.+$"
    lines = text.split('\n')
    chunks = []
    current_chunk = []
    current_header = ""
    current_length = 0
    last_index = 0

    for line in lines:
        # Détection d'un titre
        if re.match(header_pattern, line, re.MULTILINE):
            # Sauvegarder le chunk précédent
            if current_chunk:
                chunk_text = '\n'.join(current_chunk).strip()
                if chunk_text:
                    tmp_chunk = create_chunk(last_id, chunk_text, "md",
                                             file_path, last_index,
                                             last_index + len(chunk_text) - 1)
                    chunks.append(tmp_chunk)
                    last_id += 1
                    last_index += len(chunk_text) + 1

            current_header = line
            current_chunk = [line]
            current_length = len(line)
        else:
            # Vérifier la limite de taille
            if current_length + len(line) > chunk_max_size and current_chunk:
                chunk_text = '\n'.join(current_chunk).strip()
                if chunk_text:
                    tmp_chunk = create_chunk(last_id, chunk_text, "md",
                                             file_path, last_index,
                                             last_index + len(chunk_text) - 1)
                    chunks.append(tmp_chunk)
                    last_id += 1
                    last_index += len(chunk_text) + 1

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
            tmp_chunk = create_chunk(last_id, chunk_text, "md",
                                     file_path, last_index,
                                     last_index + len(chunk_text) - 1)
            chunks.append(tmp_chunk)
            last_id += 1
            last_index += len(chunk_text) + 1

    return chunks


def make_chunk_py(text: str, chunk_max_size: int,
                  last_id: int, file_path: str) -> list[Chunk]:

    lst_chunk = []
    last_index = 0

    # Initialize the chunk builder
    configs = {
        "max_chunk_size": chunk_max_size,
        "language": "python",
        "metadata_template": "default"
    }

    chunk_builder = ASTChunkBuilder(**configs)
    chunks = chunk_builder.chunkify(text)

    for i, chunk in enumerate(chunks):

        tmp_chunk = create_chunk(last_id, chunk['content'],
                                 "py", file_path,
                                 last_index,
                                 last_index + len(chunk['content']) - 1)
        lst_chunk.append(tmp_chunk)

        last_id += 1
        last_index += len(chunk['content']) + 1

    return lst_chunk


def create_chunk(id: int, text: str, fichier: str,
                 file_path: str, first_i: int, last_i: int) -> Chunk:

    dict_tmp = {
        "id": id,
        "text": text,
        "fichier": fichier,
        "file_path": file_path,
        "first_character_index": first_i,
        "last_character_index": last_i
    }

    return (Chunk(**dict_tmp))


def convert_lst_chunk_for_json(lst_chunk: list[str]) -> list[dict]:

    dict_chunk = {}
    dict_chunk = [obj.__dict__ for obj in lst_chunk]
    return (dict_chunk)
